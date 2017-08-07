from scrapper import Scrapper
from flask import Flask, render_template
from decouple import config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/bot')
def olx_bot():
    scrapper = Scrapper()
    scrapper.start()
    return render_template('sucess.html')

if __name__ == '__main__':
    if config('LOCAL', default=False, cast=bool):
        app.run(host='0.0.0.0', debug=True)
    else:
        app.run(host='0.0.0.0')