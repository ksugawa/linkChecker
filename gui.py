from tkinter import messagebox
from scraper import WebScraper
import tkinter as tk

class LinkCheckerApp:
    def __init__(self, scraper):
        self.root = tk.Tk()
        self.root.title("リンク切れ検出アプリ")
        self.root.geometry("500x280")
        self.root.columnconfigure(0, weight=1)

        # URL入力欄
        self.label = tk.Label(self.root, text="チェックするURLを入力してください。")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w")

        # フレームでテキストボックスと実行ボタンをまとめる
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.frame.columnconfigure(0, weight=1)

        # テキストボックス
        self.txtBox = tk.Entry(self.frame, width=40)
        self.txtBox.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        # 実行ボタン
        self.button = tk.Button(self.frame, text="実行", command=self.get_link)
        self.button.grid(row=0, column=1, padx=5, pady=0)

        # 進捗表示
        self.result_text = tk.Text(self.root, height=10, width=60)
        self.result_text.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # scraper インスタンスを保存
        self.scraper = scraper  # ここでscraperを受け取る

    def get_link(self):
        url = self.txtBox.get()
        print("入力されたリンク", url)
        if not url:
            messagebox.showerror("エラー", "URLを入力してください")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "リンクをチェック中...\n")

        # WebScraper に basic_url を渡す
        self.scraper.basic_url = url

        # リンクチェック
        broken_links = self.scraper.check_links(url)

        if broken_links:
            result = "\n".join(broken_links)
            self.result_text.insert(tk.END, f"リンク切れ検出:\n{result}\n")
        else:
            self.result_text.insert(tk.END, "リンク切れはありません\n")

    def run(self):
        self.root.mainloop()
