# encoding=utf8
import gc
import logging
import threading
import json, time
from decouple import config
from email_sender import send
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setExecution(param):
    Scrapper.isExecution = param


class Scrapper(threading.Thread):
    isExecution = False
    countSendMessage = 0

    def run(self):

        driver = self.getDriverWithLoggin()

        listAllLinks = []
        listAllLinks = listAllLinks + self.getLinks(driver,
                                               'http://sc.olx.com.br/florianopolis-e-regiao/'
                                               'outras-cidades/veiculos/caminhoes-onibus-e-vans'
                                               '?sd=2609&sd=2597&sd=2567&sd=2579&sd=2613&sd=2616&sd=2610&sd=2569'
                                               '&sd=2570&sd=2583&sd=2615&sd=2586&sd=2600&sd=2585&sd=2578&sd=2576'
                                               '&sd=2603&sd=2608&sd=2591&sd=2588&sd=2611&sd=2595&sd=2575&sd=2598'
                                               '&sd=2617&sd=2571&sd=2580&sd=2568&sd=2601&sd=2599&sd=2593&sd=2582'
                                               '&sd=2605&sd=2577&sd=2572&sd=2584&sd=2573&sd=2592&sd=2607&sd=2581'
                                               '&sd=2618&sd=2606&sd=2604&sd=2614&sd=2596')
        listAllLinks = listAllLinks + self.getLinks(driver,
                                               'http://sc.olx.com.br/oeste-de-santa-catarina/regioes-de-curitibanos-e-c-dos-lages/veiculos/caminhoes-onibus-e-vans')
        listAllLinks = listAllLinks + self.getLinks(driver,
                                               'http://sc.olx.com.br/norte-de-santa-catarina/veiculos/caminhoes-onibus-e-vans')

        print('Foram encontrados no total %s' % str(len(listAllLinks)))
        print('Iniciando envio de mensagens...')
        listLinksError = self.sendMessagesAndReturnErrors(driver, listAllLinks)

        driver.quit()
        driver = self.getDriverWithLoggin()

        while len(listLinksError) > 0:
            listLinksError = self.sendMessagesAndReturnErrors(driver, listLinksError)

        print('Envio de mensagens terminado')
        emailMsg = 'Olá, foi finalizado o envio dos chats, e foram enviadas %s novas mensagens!!' % str(Scrapper.countSendMessage)
        if config('LOCAL', default=False, cast=bool):
            print(emailMsg)
        else:
            print(emailMsg)
            send(config('EMAIL'), emailMsg)
        setExecution(False)


    def sendMessagesAndReturnErrors(self, driver, links):

        listLinksError = []
        chat_message = 'Caro amigo, vi que estás vendendo seu caminhão, onde caso algum cliente se interessar nele, ' \
                       'e precisar financiar uma parte, estou à disposição, faço financiamento e refinanciamento ' \
                       '(capital de giro) de caminhões usados à partir do ano de 1970, sem restrição de marca e ' \
                       'modelo, e com foco em primeiro caminhão. Estou à disposição, ' \
                       'att Oliandro Omni Financeira 48 999249090 (Tim e Whatsapp)'

        for link in links:

            gc.collect()
            if "olx.com.br" not in link:
                continue
            try:
                json.dumps(link)
                driver.get(link)

                print("Abrindo link %s" % link)
                time.sleep(5)

                showChat = driver.find_element_by_class_name('chat-client-wrapper')

                buttonShowChat = showChat.find_element_by_tag_name('button')
                buttonShowChat.click()

                chatContainer = driver.find_element_by_id('chat_container')

                listMessages = chatContainer.find_element_by_class_name('list-messages')

                time.sleep(10)

                listMessagesItens = listMessages.find_elements_by_tag_name('li')
                if len(listMessagesItens) == 0:

                    message = chatContainer.find_element_by_name('message')

                    message.send_keys(chat_message)
                    sendMessage = chatContainer.find_element_by_name('sendMessage')

                    sendMessage.click()

                    chatContainer.find_element_by_class_name('chat-close').click()

                    Scrapper.countSendMessage = Scrapper.countSendMessage + 1
                else:
                    continue
            except:  # catch *all* exceptions
                logging.exception("Erro no for de links, para o link %s" % link)
                listLinksError = listLinksError + link
                continue

        return listLinksError

    def getDriverWithLoggin(self):
        gc.enable()
        setExecution(True)
        emailOlx = config('EMAIL')
        passwordOlx = config('PASSWORD')

        print('Iniciando...')
        if config('LOCAL', default=False, cast=bool):
            driver = webdriver.Chrome()
            driver.maximize_window()
        else:
            GOOGLE_CHROME_BIN = config('GOOGLE_CHROME_BIN')
            CHROMEDRIVER_PATH = config('CHROMEDRIVER_PATH')

            chrome_options = Options()
            chrome_options.binary_location = GOOGLE_CHROME_BIN
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')

            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

        print('Realizando login...')
        driver.get('https://www3.olx.com.br/account/form_login/')

        email = driver.find_element_by_id('login_email')
        password = driver.find_element_by_id('login_password')
        login = driver.find_element_by_id('bt_submit_login')

        email.send_keys(emailOlx)
        password.send_keys(passwordOlx)

        login.click()

        print('Login realizado.')

        return driver


    def getLinks(self, driver, urlBase):
        try:
            gc.collect()
            print('Salvando pesquisa de %s.' % urlBase)

            if "?" not in urlBase:
                driver.get(urlBase + '?q=caminh%C3%A3o')
            else:
                driver.get(urlBase + '&q=caminh%C3%A3o')

            try:
                driver.find_elements_by_id('sas-interstitial')
                time.sleep(15)
            except:
                logging.exception("Nenhuma propaganda mostrada")

            listAllLinks = self.getUrl(driver)
            pagination = driver.find_element_by_class_name('module_pagination')

            listPages = pagination.find_elements_by_class_name('link')

            pagesSize = len(listPages) - 1
            for pageItem in range(pagesSize):
                url = urlBase + '?o=' + str(pageItem + 2) + '&q=caminh%C3%A3o'
                driver.get(url)

                listAllLinks = listAllLinks + self.getUrl(driver)

            return listAllLinks
        except:  # catch *all* exceptions
            logging.exception("Erro no método getLinks, para a url %s" % urlBase)


    def getUrl(self, driver):
        try:
            listAllLinks = []
            listLinks = driver.find_elements_by_class_name('OLXad-list-link')

            for link in listLinks:
                listAllLinks.append(link.get_attribute("href"))

            gc.collect()
            return listAllLinks
        except:  # catch *all* exceptions
            logging.exception("Erro no método getUrl")
