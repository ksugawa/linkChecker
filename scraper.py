import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from log import SaveLog

class WebScraper:
    def __init__(self, login_info, progress_callback=None):
        self.session = requests.Session()
        self.login_info = login_info
        self.h_files = set()      # 調査済URL リスト
        self.page_link = set()    # 探索対象URL リスト
        self.checked_link = set() # 探索済URL リスト
        self.basic_url = ""       # 入力されたURL
        self.progress_callback = progress_callback


    def login(self):
        # ログイン処理（ここでは省略）
        pass

    def extract_title(self, res):
        # ページタイトルを取得
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.find('title')
        return title.string.strip() if title and title.string else ''

    def get_links_from_page(self, soup):
        # ページ内のリンクを取得し、探索対象URLリストに追加
        links = []
        for link in soup.find_all('a', href=True):
            url = link.get('href')
            if url is None or url == '#':
                continue

            url = urljoin(self.basic_url, url)
            link_text = link.get_text(strip=True).replace(',', ' ') if link.get_text(strip=True) else 'リンクテキストなし'
            print("リンクテキスト:", link_text)

            # 重複防止
            if url in self.h_files or url in self.page_link or url in self.checked_link:
                continue

            links.append((url, link_text))
            self.page_link.add(url)
        return links

    def check_url(self, url):
        # ステータスコードを取得
        if url in self.checked_link:
            return 'skipped', ''
        
        try:
            res = self.session.get(url, timeout=(5.0, 7.5))
            self.checked_link.add(url)

            if 'docs.google.com' in url or 'drive.google.com' in url:
                return '403', 'googleDrive'
            return str(res.status_code), ''
        except requests.exceptions.RequestException:
            return 'timeout', ''

    def process_page(self, res, app):
        # ページ内のリンクを処理
        soup = BeautifulSoup(res.content, 'html.parser')
        links = self.get_links_from_page(soup)
        
        title_text = self.extract_title(res)
        print("ページタイトル: ", title_text)

        total_links = len(links)
        all_links_info = []

        for index, (url, link_text) in enumerate(links, start=1):
            if not app.running:
                print("キャンセルが押されたため中断")
                return []
            
            link_kind = '内部リンク' if url.startswith(self.basic_url) else '外部リンク'
            status, option = self.check_url(url)

            if status != 'skipped':
                all_links_info.append((url, link_text, link_kind, option, status))

            # 進捗を更新
            if self.progress_callback:
                self.progress_callback(index, total_links)

        SaveLog(title_text, all_links_info).write_to_xlsx()
        return links

    def check_links(self, url, app):
        # メイン処理
        self.basic_url = url
        res = self.session.get(self.basic_url)

        if self.progress_callback:
            self.progress_callback(0, 1)

        return self.process_page(res, app)