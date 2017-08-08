# encoding=utf8
import threading
from selenium import webdriver
from decouple import config
import json, time
from email_sender import send
from selenium.webdriver.chrome.options import Options

class Scrapper(threading.Thread):
    def run(self):

        emailOlx = config('EMAIL')
        passwordOlx = config('PASSWORD')

        if config('LOCAL', default=False, cast=bool):
            driver = webdriver.Chrome()
        else:
            GOOGLE_CHROME_BIN = config('GOOGLE_CHROME_BIN')
            CHROMEDRIVER_PATH = config('CHROMEDRIVER_PATH')

            chrome_options = Options()
            chrome_options.binary_location = GOOGLE_CHROME_BIN
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')

            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

        driver.get('https://www3.olx.com.br/account/form_login/')

        email = driver.find_element_by_id('login_email')
        password = driver.find_element_by_id('login_password')
        login = driver.find_element_by_id('bt_submit_login')

        email.send_keys(emailOlx)
        password.send_keys(passwordOlx)

        login.click()

        chat_message = 'Caro amigo, vi que estás vendendo seu caminhão, onde caso algum cliente se interessar nele, ' \
                       'e precisar financiar uma parte, estou à disposição, faço financiamento e refinanciamento ' \
                       '(capital de giro) de caminhões usados à partir do ano de 1970, sem restrição de marca e ' \
                       'modelo, e com foco em primeiro caminhão. Estou à disposição, ' \
                       'att Oliandro Omni Financeira 48 999249090 (Tim e Whatsapp)'
                        
        listAllLinks = []
        listAllLinks = listAllLinks + getLinks(driver,
                                               'http://sc.olx.com.br/florianopolis-e-regiao/grande-florianopolis/veiculos')
        listAllLinks = listAllLinks + getLinks(driver,
                                               'http://sc.olx.com.br/florianopolis-e-regiao/outras-cidades/veiculos')
        listAllLinks = listAllLinks + getLinks(driver,
                                               'http://sc.olx.com.br/oeste-de-santa-catarina/regioes-de-curitibanos-e-c-dos-lages/veiculos')
        listAllLinks = listAllLinks + getLinks(driver, 'http://sc.olx.com.br/norte-de-santa-catarina/veiculos/')

        countSendMessage = 0
        for link in listAllLinks:
            json.dumps(link)
            driver.get(link)

            showChat = driver.find_element_by_class_name('chat-client-wrapper')

            buttonShowChat = showChat.find_element_by_tag_name('button')
            buttonShowChat.click()

            chatContainer = driver.find_element_by_id('chat_container')

            listMessages = chatContainer.find_element_by_class_name('list-messages')

            time.sleep(5)

            listMessagesItens = listMessages.find_elements_by_tag_name('li')
            if len(listMessagesItens) == 0:

                message = chatContainer.find_element_by_name('message')

                message.send_keys(chat_message)
                sendMessage = chatContainer.find_element_by_name('sendMessage')

                sendMessage.click()

                chatContainer.find_element_by_class_name('chat-close').click()

                countSendMessage = countSendMessage + 1
            else:
                continue

        emailMsg = 'Olá, foi finalizado o envio dos chats, e foram enviadas ' + \
                   str(countSendMessage) + ' novas mensagens!!'
        send(emailOlx, emailMsg)

def getLinks(driver, urlBase):

    driver.get(urlBase + '?q=caminh%C3%A3o')

    listAllLinks = getUrl(driver)
    pagination = driver.find_element_by_class_name('module_pagination')

    listPages = pagination.find_elements_by_class_name('link')

    pagesSize = len(listPages) - 1
    for pageItem in range(pagesSize):
        url = urlBase + '?o=' + str(pageItem + 2) + '&q=caminh%C3%A3o'
        driver.get(url)

        listAllLinks = listAllLinks + getUrl(driver)

    return listAllLinks

def getUrl(driver):

    listAllLinks = []
    listLinks = driver.find_elements_by_class_name('OLXad-list-link')

    for link in listLinks:
        listAllLinks.append(link.get_attribute("href"))

    return listAllLinks
