from flask import Flask
from dotenv import load_dotenv
import os
from waitress import serve
from flask import render_template

from blueprints import typhoonAlarm_bp
from blueprints import Login_bp

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(typhoonAlarm_bp)
app.register_blueprint(Login_bp)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 200))
    print(f"Starting Flask application on {host}:{port}")
    serve(app, host=host, port=port)
    #app.run(debug=True, host=host, port=port)