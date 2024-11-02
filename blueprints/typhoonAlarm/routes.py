from . import typhoonAlarm_bp
from flask import render_template, redirect, url_for, request, session
from .typhoon_search import TyphoonSearch


@typhoonAlarm_bp.route('/typhoonAlarm', methods=['POST', 'GET'])
def typhoonAlarm():
    # 獲取 session 中的數據
    city_data = session.pop('city_data', None)
    update_time = session.pop('update_time', None)
    message = session.pop('message', None)
    execution_time = session.pop('execution_time', None)
    return render_template('typhoonAlarm.html', city_data=city_data, update_time=update_time, message=message, execution_time=execution_time)

@typhoonAlarm_bp.route('/typhoonAlarm_search', methods=['POST'])
def typhoonAlarm_search():
    city = request.form.get("cities")
    if not city:
        session['message'] = '請選取表單中的縣市'
        return redirect(url_for('typhoonAlarm.typhoonAlarm'))

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

    return redirect(url_for('typhoonAlarm.typhoonAlarm'))