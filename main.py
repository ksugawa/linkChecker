from gui import LinkCheckerApp
from scraper import WebScraper
import datetime


if __name__ == "__main__":
    now = datetime.datetime.now()  # 時間まで
    fname = 'test' + now.strftime('%Y%m%d%H%M%S') + '.csv'

    # ID&PASS
    ID = "your_id"
    PASS = "your_pass"

    # Basic認証情報
    login_info = {"ID": ID, "pass": PASS}

    # WebScraperの初期化（login_infoとfnameを渡す）
    scraper = WebScraper(login_info, fname)

    # アプリ実行
    app = LinkCheckerApp(scraper)
    app.run()
