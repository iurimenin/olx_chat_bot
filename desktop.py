from scrapper import Scrapper

# Desktop Version
def olx_bot():
    scrapper = Scrapper()

    if (Scrapper.isExecution):
       print('O Programa já está sendo executado')
    else:
        scrapper.start()
        print('O Programa está sedo iniciado')


if __name__ == '__main__':
   olx_bot()