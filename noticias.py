import requests
from bs4 import BeautifulSoup
import datetime
from cryptos import crypto_price, variacao_bitcoin
from API_Twitter import api

def popular_news(x) :
    #Aqui ele solicita o HTML da página.
    p1 = requests.get('https://livecoins.com.br/noticias/?filter_by=popular' + x)
    pagina = p1.content
    #Aqui ele vai procurar especificamente as notícias.
    soup1 = BeautifulSoup (pagina, 'html.parser')
    noticias = soup1.find_all('h3', class_='entry-title td-module-title')
    agora = 0
    max = 5
    noticia = []
    lista_noticias = []
    while agora != max:
        n = noticias[agora].find ('a')
        link = n['href']
        titulo = n['title']
        noticia.append (titulo)
        noticia.append (link)
        lista_noticias.append (noticia)
        noticia = []
        agora += 1
    return lista_noticias

def get_week_day() :
    #Aqui na verdade é totalmente inútil atualmente, eu ia usar pra pegar noticias antigas mas talvez não use.
    days = {0 : 'Segunda',
            1 : 'Terca',
            2 : 'Quarta',
            3 : 'Quinta',
            4 : 'Sexta',
            5 : 'Sabado',
            6 : 'Domingo'}
    dia = days[datetime.datetime.today ().weekday ()]
    return dia

def noticias_populares() :
    #Se for sexta, ele vai solicitar as noticias populares dos ultimos 7 dias, qualquer outro dia só solicita as principais das ultimas 24 horas.
    if get_week_day() == 'Sexta':
        return popular_news('7')
    else :
        return popular_news('1')

def boletim_bitcoin():
    noticias_populares()
    #Aqui ta Sexta mas se quiser modificar pode modificar por 'if datetime.datetime.today().weekday() == 4: '
    if get_week_day() == 'Sexta':
        api.update_status(f'Boa tarde, esse é o seu boletim semanal sobre criptomoedas!\n'
              f'O Bitcoin fecha o dia em ${crypto_price("bitcoin"):.2f} Dólares, {variacao_bitcoin()} em relação a ontem, confira na Thread as principais notícias da semana!\n'
                          f'Tenha uma ótima Sexta-Feira!')
    else:
        api.update_status(f'Boa tarde, este é o seu boletim diário sobre criptomoedas!\n'
              f'O Bitcoin fecha o dia em ${crypto_price("bitcoin"):.2f} Dólares, {variacao_bitcoin()} em relação a ontem, confira na Thread as principais notícias do dia!')

    for x in noticias_populares():
        #Aqui é o jeito que eu consegui de fazer thread, ele vai sempre responder o ultimo tweet feito pela conta, no caso é o tweet do boletim.
        get_user = api.get_user('@hublibertario')
        last_tweet = api.user_timeline(get_user.id)
        last_tweet_id = last_tweet[0].id
        api.update_status(f'{x[0]}\n{x[1]}', last_tweet_id)
