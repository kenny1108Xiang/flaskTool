from flask import Flask
from dotenv import load_dotenv
import os
from waitress import serve
from typhoon_search import TyphoonSearch
from flask import render_template, request, redirect, url_for, session

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



@app.route('/')
def index():
    # 獲取 session 中的數據
    city_data = session.pop('city_data', None)
    update_time = session.pop('update_time', None)
    message = session.pop('message', None)
    execution_time = session.pop('execution_time', None)
    return render_template('index.html', city_data=city_data, update_time=update_time, message=message, execution_time=execution_time)

@app.route('/search', methods=['POST'])
def search():
    city = request.form.get("cities")
    if not city:
        session['message'] = '請選取表單中的縣市'
        return redirect(url_for('index'))

    _search = TyphoonSearch()
    result = _search.search_city(city)

    # 如果找不到結果
    if result["city_data"] is None:
        session['message'] = f"找不到該縣市 '{city}'"
    else:
        # 如果找到結果，將結果存入 session
        session['city_data'] = ', '.join(result["city_data"])  # 將 city_data 轉為字符串
        session['update_time'] = result["update_time"]
    
    # 無論是否找到結果，都存入執行時間
    session['execution_time'] = f"響應時間 {result['execution_time']:.3f} 毫秒"

    # 重定向到 index 路由
    return redirect(url_for('index'))

if __name__ == '__main__':
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 200))
    print(f"Starting Flask application on {host}:{port}")
    serve(app, host=host, port=port)
