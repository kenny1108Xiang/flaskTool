from . import airQuality_bp
from flask import render_template, request
from .airQuality_search import airQuality
from datetime import datetime, timedelta

air_api = airQuality()

@airQuality_bp.route('/airQuality', methods=['POST', 'GET'])
def AirQuality():
    return render_template('AirQuality.html')

@airQuality_bp.route('/airQuality_search', methods=['POST', 'GET'])
def airQuality_search():
    message = None
    air_data = None
    execution_time = None

    if request.method == 'POST':
        city = request.form.get('city')
        district = request.form.get('district')

        # 確認 city 和 district 都已選擇
        if not city or not district:
            message = "請選擇縣市與地區"
        else:
            # 獲取空氣品質資料
            air_data_message, execution_time = air_api.get_air_quality(city, district)
            execution_time = f"響應時間 {execution_time:.3f} 毫秒"

            # 將 `air_data_message` 轉換成字典格式並格式化發布時間
            air_data = {}
            try:
                for item in air_data_message.split(", "):
                    key, value = item.split(": ")
                    if key.strip() == "發布時間":
                        # 解析時間並減去一小時
                        publish_time = datetime.strptime(value.strip(), "%Y/%m/%d %H:%M") - timedelta(hours=1)
                        
                        # 手動將 AM/PM 和星期轉換為中文
                        days_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
                        day_name = days_of_week[publish_time.weekday()]
                        
                        hour = publish_time.hour
                        period = "上午" if 0 <= hour < 12 else "下午" if hour < 18 else "晚上"
                        formatted_hour = hour % 12 if hour % 12 != 0 else 12
                        
                        # 格式化為指定的字串格式
                        air_data["發布時間"] = f"{publish_time.strftime('%Y/%m/%d')} {day_name} {period}{formatted_hour}點"
                    else:
                        air_data[key.strip()] = value.strip()
            except ValueError:
                message = "資料格式錯誤"
                air_data = None

    return render_template(
        'AirQuality.html',
        message=message,
        air_data=air_data,
        city=city,
        district=district,
        execution_time=execution_time
    )