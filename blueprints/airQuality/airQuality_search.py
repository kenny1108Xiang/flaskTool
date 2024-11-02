import requests
from datetime import datetime
import os
import time

class airQuality:
    def __init__(self):
        self.api_key = os.getenv("api_token_air")
        self.air_url = f"https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key={self.api_key}&limit=1000&sort=ImportDate%20desc&format=JSON"

    def get_air_quality(self, city: str, district: str):
        # 計時開始
        time_cont = time.perf_counter()

        # 發送請求
        response = requests.get(self.air_url)
        data = response.json()

        # 篩選數據
        filtered_data = [
            {
                "sitename": record["sitename"],
                "status": record["status"],
                "pm2.5": record["pm2.5"],
                "publishtime": datetime.strptime(record["publishtime"], "%Y/%m/%d %H:%M:%S").strftime("%Y/%m/%d %H:%M")
            }
            for record in data["records"]
            if record["county"] == city and record["sitename"] == district
        ]

        # 處理查詢結果
        if filtered_data:
            message = "\n".join(
                f"測站名稱: {item['sitename']}, 狀態: {item['status']}, PM2.5: {item['pm2.5']}, 發布時間: {item['publishtime']}"
                for item in filtered_data
            )
        else:
            message = f"找不到指定的 {city} 縣市中的 {district} 測站。"

        # 計時結束
        end_time = time.perf_counter()
        execution_time = (end_time - time_cont) * 1000  # 轉換為毫秒

        return message, execution_time
