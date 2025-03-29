from gui import LinkCheckerApp
from scraper import WebScraper

if __name__ == "__main__":
    # ID&PASS
    ID = "your_id"
    PASS = "your_pass"

    # Basic認証情報
    login_info = {"ID": ID, "pass": PASS}

    # WebScraperの初期化（login_infoとfnameを渡す）
    scraper = WebScraper(login_info)

    # アプリ実行
    app = LinkCheckerApp(scraper)
    app.run()
