from tkinter import messagebox, ttk
from scraper import WebScraper
import tkinter as tk
import threading

class LinkCheckerApp:
    def __init__(self, scraper: WebScraper):
        self.root = tk.Tk()
        self.root.title("リンク切れ検出アプリ")
        self.root.geometry("500x150")
        self.root.columnconfigure(0, weight=1)

        # フレームでテキストボックス、ボタン、プログレスバーをまとめる
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(0, weight=1)

        # URL入力欄
        self.label = tk.Label(self.frame, text="チェックするURLを入力してください。", font=("Helvetica", 9))
        self.label.grid(row=0, column=0, columnspan=2, padx=(0, 5), pady=(5, 0), sticky="w")

        # テキストボックス
        self.txtBox = tk.Entry(self.frame, width=40, font=("Helvetica", 11))
        self.txtBox.grid(row=1, column=0, padx=(0, 5), pady=0, sticky="ew")

        # 実行ボタン
        self.button = tk.Button(self.frame, text="実行", command=self.start_check)
        self.button.grid(row=1, column=1, padx=5, pady=0, sticky="ew")

        # 進捗情報ラベル
        self.progress_label = tk.Label(self.frame, text="0 / 0 ページチェック済み", font=("Helvetica", 9))
        self.progress_label.grid(row=2, column=0, padx=(0, 5), pady=(10, 0), sticky="w")

        # プログレスバー
        self.progbar = ttk.Progressbar(self.frame, mode="determinate")
        self.progbar.grid(row=3, column=0, padx=(0, 5), pady=5, sticky="ew")

        # キャンセルボタン
        self.button_cancel = tk.Button(self.frame, text="キャンセル", command=self.cancel_check)
        self.button_cancel.grid(row=3, column=1, padx=5, pady=0, sticky="ew")

        # scraper インスタンスを保存
        self.scraper = scraper

        # 実行中フラグ
        self.running = False

    def update_progress(self, current, total):
        # スクレイピング進捗をプログレスバーに反映
        progress = int((current / total) * 100) if total > 0 else 0
        self.progbar["value"] = progress
        self.progress_label.config(text=f"{current} / {total} ページチェック済み")
        self.root.update_idletasks()

    def start_check(self):
        # 実行ボタンが押された時の処理
        url = self.txtBox.get()
        print("入力されたリンク", url)
        if not url:
            messagebox.showerror("エラー", "URLを入力してください")
            return
        
        self.progbar["value"] = 0
        self.running = True  # 実行フラフをセット

        self.scraper.basic_url = url
        self.scraper.progress_callback = self.update_progress

        # スクレイピング処理を別スレッドで実行
        thread = threading.Thread(target=self.run_check, args=(url,))
        thread.start()
        
    def run_check(self, url):
        # スクレイピング実行
        all_links = self.scraper.check_links(url, self)

        if self.running:
            broken_links = [link for link, status in all_links if status in ('404', 'timeout')]

            if broken_links:
                messagebox.showerror("エラー", f"リンク切れ検出: {len(broken_links)} 件")
            else:
                messagebox.showinfo('完了', 'リンク切れはありません')
        
        self.running = False # 処理が終了したらフラグをリセット

    def cancel_check(self):
        # キャンセルボタンが押された時の処理
        self.running = False
        messagebox.showinfo("キャンセル", "処理を中断しました。")

    def run(self):
        self.root.mainloop()
