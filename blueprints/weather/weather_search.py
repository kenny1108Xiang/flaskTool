import requests
from datetime import datetime
import os
import time

class Weather:
    def __init__(self):
        self.api_token = os.getenv("api_token")
        self.weather_url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={self.api_token}&format=JSON"

    def get_weather(self, city: str):
        # 計時開始
        time_cont = time.perf_counter()

        response = requests.get(self.weather_url)
        
        if response.status_code != 200:
            print("無法取得天氣資料")
            return None
        
        data_json = response.json()

        # 查找指定的城市資料
        location_data = None
        for location in data_json['records']['location']:
            if location['locationName'] == city:
                location_data = location
                break

        if not location_data:
            print(f"找不到城市 {city} 的天氣訊息。")
            return None

        # 解析天氣要素
        weather_elements = location_data['weatherElement']
        periods = {}

        for element in weather_elements:
            element_name = element['elementName']
            for time_entry in element['time']:
                # 轉換和格式化開始和結束時間
                start_time = datetime.strptime(time_entry['startTime'], "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(time_entry['endTime'], "%Y-%m-%d %H:%M:%S")

                # 格式化日期和星期
                start_day = start_time.strftime("%Y-%m-%d") + f" 星期{self.get_chinese_weekday(start_time)}"
                end_day = end_time.strftime("%Y-%m-%d") + f" 星期{self.get_chinese_weekday(end_time)}"

                # 格式化時間
                start_formatted = self.format_hour(start_time)
                end_formatted = self.format_hour(end_time)

                # 合併格式化的日期和時間
                period_key = f"{start_day} {start_formatted} -\n{end_day} {end_formatted}"
                
                if period_key not in periods:
                    periods[period_key] = {}
                periods[period_key][element_name] = time_entry['parameter']['parameterName']
        
        # 計時結束
        end_time = time.perf_counter()
        execution_time = (end_time - time_cont) * 1000  # 轉換為毫秒

        return periods, execution_time  # 返回解析後的天氣資料字典

    def format_hour(self, dt):
        """將時間轉換為中文格式，例如晚上 6 點或早上 6 點"""
        hour = dt.hour
        if hour == 6:
            return "早上 6 點"
        elif hour == 18:
            return "晚上 6 點"
        elif hour == 0:
            return "凌晨 12 點"
        elif hour == 12:
            return "中午 12 點"
        elif 0 < hour < 12:
            return f"早上 {hour} 點"
        else:
            return f"下午 {hour - 12} 點"

    def get_chinese_weekday(self, dt):
        """將星期轉換為中文格式，0 是星期一，6 是星期日"""
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        return weekdays[dt.weekday()]
