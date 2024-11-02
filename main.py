from flask import Flask
from dotenv import load_dotenv
import os
from waitress import serve
from flask import render_template

from blueprints import typhoonAlarm_bp
from blueprints import Login_bp
from blueprints import Weather_bp
from blueprints import airQuality_bp

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(typhoonAlarm_bp)
app.register_blueprint(Login_bp)
app.register_blueprint(Weather_bp)
app.register_blueprint(airQuality_bp)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/404NotFound')
def NotFound_Page():
    return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    # 渲染自定義的 404 模板
    return render_template('404.html'), 404

if __name__ == '__main__':
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 200))
    print(f"Starting Flask application on {host}:{port}")
    #serve(app, host=host, port=port)
    app.run(debug=True, host=host, port=port)