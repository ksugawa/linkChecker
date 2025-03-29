import os
import datetime
from tkinter import filedialog
from openpyxl import Workbook

class SaveLog:
    def __init__(self, title_text, log_data):
         self.output_file = ""           # ログ用EXCEL
         self.log_data = log_data
         self.title_text = title_text

    def write_to_xlsx(self):
            # ログをEXCELに出力
            if not self.log_data:
                return []
            
            now = datetime.datetime.now()

            logs_dir = os.path.join(os.getcwd(), "logs")
            os.makedirs(logs_dir, exist_ok=True)

            self.output_file = os.path.join(logs_dir, f'linkCheckLog_{self.title_text}_{now.strftime("%Y%m%d%H%M%S")}.xlsx')

            wb = Workbook()
            ws = wb.active
            ws.append(["URL", "リンクテキスト", "リンク種別", "オプション", "ステータス"])

            for log in self.log_data:
                ws.append(log)

            wb.save(self.output_file)