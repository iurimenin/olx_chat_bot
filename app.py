from scrapper import Scrapper
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/bot')
def olx_bot():
    scrapper = Scrapper()
    scrapper.start()
    return render_template('sucess.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)