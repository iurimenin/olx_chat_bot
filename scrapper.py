# encoding=utf8
import gc
import logging
import threading
import json, time
from decouple import config
from email_sender import send
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scrapper(threading.Thread):
    isExecution = False
    countSendMessage = 0
    url = ''
    local = ''

    def run(self):

        driver = self.get_driver_with_loggin()

        listAllLinks = []
        listAllLinks = listAllLinks + self.get_links(driver, Scrapper.url)

        print('Foram encontrados no total %s para %s' % (str(len(listAllLinks)), Scrapper.local))
        print('Iniciando envio de mensagens...')
        listLinksError = self.sendMessagesAndReturnErrors(driver, listAllLinks)

        driver.quit()
        driver = self.get_driver_with_loggin()

        while len(listLinksError) > 0:
            listLinksError = self.sendMessagesAndReturnErrors(driver, listLinksError)

        print('Envio de mensagens terminado')
        emailMsg = 'Olá, foi finalizado o envio dos chats, e foram enviadas %s novas mensagens para %s!!' \
                   % (str(Scrapper.countSendMessage), Scrapper.local)
        if config('LOCAL', default=False, cast=bool):
            print(emailMsg)
        else:
            print(emailMsg)
            send(config('EMAIL'), emailMsg)
            Scrapper.isExecution = False

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
                listLinksError.append(link)
                continue

        return listLinksError

    def get_driver_with_loggin(self):
        gc.enable()
        Scrapper.isExecution = True
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

    def get_links(self, driver, urlBase):
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

            listAllLinks = self.get_links_url(driver)
            pagination = driver.find_element_by_class_name('module_pagination')

            listPages = pagination.find_elements_by_class_name('link')

            pagesSize = len(listPages) - 1
            for pageItem in range(pagesSize):
                if "?" not in urlBase:
                    url = urlBase + '?o=' + str(pageItem + 2) + '&q=caminh%C3%A3o'
                else:
                    url = urlBase + '&o=' + str(pageItem + 2) + '&q=caminh%C3%A3o'
                driver.get(url)

                listAllLinks = listAllLinks + self.get_links_url(driver)

            return listAllLinks
        except:  # catch *all* exceptions
            logging.exception("Erro no método getLinks, para a url %s" % urlBase)

    def get_links_url(self, driver):
        try:
            listAllLinks = []
            listLinks = driver.find_elements_by_class_name('OLXad-list-link')

            for link in listLinks:
                listAllLinks.append(link.get_attribute("href"))

            gc.collect()
            return listAllLinks
        except:  # catch *all* exceptions
            logging.exception("Erro no método getUrl")
