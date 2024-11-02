from . import Weather_bp
from flask import render_template, request
from .weather_search import Weather
# 初始化 Weather 類別

weather_api = Weather()

@Weather_bp.route('/weather', methods=['POST', 'GET'])
def weather():
    return render_template('weather.html')

@Weather_bp.route('/weather_search', methods=['POST', 'GET'])
def weather_search():
    city_data = None
    message = None
    city = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            # 呼叫 Weather 類別的 get_weather 方法取得天氣資料
            city_data, execution_time = weather_api.get_weather(city)
            execution_time = f"響應時間 {execution_time:.3f} 毫秒"
            if not city_data:
                message = f"找不到城市 {city} 的天氣訊息。"
        else:
            message = "請選擇一個縣市進行查詢。"
    
    # 將資料傳遞給模板
    return render_template('weather.html', city=city, city_data=city_data, message=message, execution_time=execution_time)
