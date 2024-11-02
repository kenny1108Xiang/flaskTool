import requests
from bs4 import BeautifulSoup
import time

class TyphoonSearch:
    def __init__(self):
        self.url = "https://www.dgpa.gov.tw/typh/daily/nds.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        self.data, self.update_time, self.execution_time = self._fetch_data()

    def _fetch_data(self):
        # 計時開始
        start_time = time.perf_counter()

        # 發送請求並取得網頁內容
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'utf-8'  # 設置編碼，確保中文顯示正確
        html_content = response.text

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # 查找 class=Table_Body 的 tbody
        tbody = soup.find("tbody", class_="Table_Body")

        update_time_div = soup.find("div", class_="f_right Content_Updata")
        if update_time_div:
            h4_tag = update_time_div.find("h4")
            if h4_tag:
                # 提取非 <a> 標籤的文字內容
                update_time = ''.join([
                    text for text in h4_tag.strings if text.parent.name != 'a'
                ]).strip()
            else:
                update_time = "無更新時間資訊"
        else:
            update_time = "無更新時間資訊"

        # 查找 tbody 中的前 22 個 tr
        rows = tbody.find_all("tr")[:22] if tbody else []

        # 解析表格數據
        data = []
        for row in rows:
            tr_data = [font.text.strip() for font in row.find_all("font")]
            if tr_data:
                data.append(tr_data)

        # 計時結束
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # 轉換為毫秒

        return data, update_time, execution_time

    def search_city(self, city_name):
        """
        輸入縣市名稱\n
        台或臺都可以，會進行自動替換\n
        回傳資料包含 'city_data'、'update_time' 與 'execution_time'，可根據需要抓取\n
        """
        # 將 '台' 替換為 '臺'，確保查詢的一致性
        city_name = city_name.replace('台', '臺')
        
        # 搜尋符合的縣市資料
        for tr_data in self.data:
            if city_name in tr_data[0]:  # 假設第一個 font 包含縣市名稱
                return {
                    "city_data": tr_data,
                    "update_time": self.update_time,
                    "execution_time": self.execution_time
                }
        
        # 若無找到則回傳 None 並附上更新時間和執行時間
        return {
            "city_data": None,
            "update_time": self.update_time,
            "execution_time": self.execution_time
        }
