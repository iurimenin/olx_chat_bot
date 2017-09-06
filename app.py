# encoding=utf8
from decouple import config
from scrapper import Scrapper
from flask import Flask, render_template

app = Flask(__name__)
# Web version
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/floripa')
def floripa():
    scrapper = Scrapper()

    if (Scrapper.isExecution):
        return render_template('running.html')
    else:
        Scrapper.url = 'http://sc.olx.com.br/florianopolis-e-regiao/' \
                       'outras-cidades/veiculos/caminhoes-onibus-e-vans' \
                                               '?sd=2609&sd=2597&sd=2567&sd=2579&sd=2613&sd=2616&sd=2610&sd=2569' \
                                               '&sd=2570&sd=2583&sd=2615&sd=2586&sd=2600&sd=2585&sd=2578&sd=2576' \
                                               '&sd=2603&sd=2608&sd=2591&sd=2588&sd=2611&sd=2595&sd=2575&sd=2598' \
                                               '&sd=2617&sd=2571&sd=2580&sd=2568&sd=2601&sd=2599&sd=2593&sd=2582' \
                                               '&sd=2605&sd=2577&sd=2572&sd=2584&sd=2573&sd=2592&sd=2607&sd=2581' \
                                               '&sd=2618&sd=2606&sd=2604&sd=2614&sd=2596'

        Scrapper.local = 'Florianópolis e região'

        scrapper.start()
        return render_template('sucess.html')


@app.route('/oeste')
def oeste():
    scrapper = Scrapper()

    if (Scrapper.isExecution):
        return render_template('running.html')
    else:
        Scrapper.url = 'http://sc.olx.com.br/oeste-de-santa-catarina/' \
                       'regioes-de-curitibanos-e-c-dos-lages/veiculos/caminhoes-onibus-e-vans'
        Scrapper.local = 'Oeste de Santa Catarina'
        scrapper.start()
        return render_template('sucess.html')


@app.route('/norte')
def norte():
    scrapper = Scrapper()

    if (Scrapper.isExecution):
        return render_template('running.html')
    else:
        Scrapper.url = 'http://sc.olx.com.br/norte-de-santa-catarina/veiculos/caminhoes-onibus-e-vans'
        Scrapper.local = 'Norte de Santa Catarina'
        scrapper.start()
        return render_template('sucess.html')

if __name__ == '__main__':
    if config('LOCAL', default=False, cast=bool):
        app.run(host='0.0.0.0', debug=True)
    else:
        app.run(host='0.0.0.0')