import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import codecs

class WebScraper:
    def __init__(self, login_info, fname):
        self.session = requests.Session()
        self.login_info = login_info
        self.fname = fname
        self.basic_url = ""  # 入力されたURLを保存

    def login(self):
        # ログイン処理（ここでは省略）
        pass

    def extract_title(self, res):
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.find('title')
        if title and title.string:
            return title.string.strip()
        return ''

    def get_links_from_page(self, soup):
        links = []
        for link in soup.find_all('a', href=True):
            url = link.get('href')
            if url is None or url == '#':
                continue
            link_text = str(link.string).replace(',', ' ') if link.string else ''
            print("リンクテキスト:", link_text)
            url = urljoin(self.basic_url, url)  # base_urlをbasic_urlに変更
            links.append((url, link_text))
        return links

    def check_url(self, url):
        try:
            res = self.session.get(url, timeout=(5.0, 7.5))
            if 'docs.google.com' in url or 'drive.google.com' in url:
                return '403', 'googleDrive'
            return str(res.status_code), ''
        except requests.exceptions.RequestException:
            return 'timeout', ''

    def write_to_csv(self, link_text, status, url, link_kind, option=''):
        logs_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        file_path = os.path.join(logs_dir, self.fname)

        with codecs.open(file_path, 'a', encoding='utf-8-sig', errors='ignore') as f:
            f.write(f"{link_text},{status},{url},{link_kind}{option}\n")

    def process_page(self, res):
        title_text = self.extract_title(res)
        print(title_text)
        soup = BeautifulSoup(res.content, 'html.parser')
        links = self.get_links_from_page(soup)

        for url, link_text in links:
            link_kind = '内部リンク' if url.startswith(self.basic_url) else '外部リンク'
            status, option = self.check_url(url)
            self.write_to_csv(link_text, status, url, link_kind, option)

    def check_links(self, url):
        self.basic_url = url  # 受け取ったURLをbasic_urlにセット
        res = self.session.get(self.basic_url)  # basic_urlを使ってリクエストを送信
        self.process_page(res)
        return []  # 実際のリンク切れをリストとして返す部分を実装してください
