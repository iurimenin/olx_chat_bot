# olx_chat_bot

Chat bot para enviar mensagens automaticas no OLX.

Para executar localmente:
* Criar um arquivo chamado .env para adicionar as váriaveis de ambiente.
* Deve ser baixado e adicionado o chromedriver na pasta bin da sua virtualenv ou configurar o caminho correto para o mesmo

Para executar no Heroku:
* Adicionar os seguintes Buildpacks
  * https://github.com/heroku/heroku-buildpack-xvfb-google-chrome.git
  * https://github.com/heroku/heroku-buildpack-chromedriver.git
  * heroku/python
* Mudar o stack para cedar-14 

Váriaveis de ambiente:
* LOCAL=True (Somente adicionar no arquivo .env, no heroku não é nescesário ou deve ser false)
* EMAIL=E-mail da Olx
* PASSWORD=Senha da Olx
* EMAILSENDER=E-mail para ser o remetente ao fim da execução
* PASSWORDSENDER=Senha do e-mail remetente

OBS: Está fixo no código uma pesquisa "caminhão", para uma região especifica de Santa Catarina.
