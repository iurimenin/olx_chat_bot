# olx_chat_bot

Chat bot para enviar mensagens automaticas no OLX.

Para rodar tanto locamente quanto no heroku devem ser configuradas as seguintes variaveis de ambiente:

* LOCAL=True para ver o navegador e False para rodar sem a parte visual
* EMAIL=E-mail da Olx
* PASSWORD=Senha da Olx
* EMAILSENDER=E-mail para ser o remetente ao fim da execução
* PASSWORDSENDER=Senha do e-mail remetente

*Para LOCAL:*
* Deve ser baixado e adicionado o chromedriver na pasta bin da sua virtualenv ou configurar o caminho correto para o mesmo

Para Heroku:
* Adicionar os seguintes Buildpacks
  * https://github.com/heroku/heroku-buildpack-xvfb-google-chrome.git
  * https://github.com/heroku/heroku-buildpack-chromedriver.git
  * heroku/python
* Mudar o stack para cedar-14 


OBS: Está fixo no código uma pesquisa "caminhão", para uma região especifica de Santa Catarina.
