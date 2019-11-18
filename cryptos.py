import requests
import database
##É daqui onde está tirando a informação de todas as cryptos.
ticker_api_url = 'https://api.coinmarketcap.com/v1/ticker/'

def crypto_price(crypto):
    if crypto =='todos':
        crypto_str_final = all_cryptos()
        return crypto_str_final
    else:
        price = get_latest_crypto_price(crypto)
        return price

def get_latest_crypto_price( crypto ):
    response = requests.get(ticker_api_url+crypto)
    response_json = response.json()
    if crypto == '':
        #Irá retornar um json com todas as cryptos monitoradas.
        return response_json
    else:
        #Retorna somente o preço da moeda.
        return float(response_json[0]['price_usd'])
def all_cryptos():
    #É só adicionar o id d criptomoeda que automaticamente o código começa a monitorar ela
    crypto_ids = ['bitcoin', 'ethereum', 'nano', 'litecoin', 'monero', 'dash']
    cryptos = list()
    crypto_info = list()
    crypto_str_final = ''
    for x in get_latest_crypto_price(''):
        if x['id'] in crypto_ids:
            cryptos.append(x['name'])
            cryptos.append(x['price_usd'])
            crypto_info.append(cryptos)
            cryptos = list()
    for x in crypto_info:
        ##Aqui eu dividi em dois pois o \n estava conflitando com a API do twitter
        if x[0] == 'Nano':
            crypto_str = f'{x[0]}: ${float(x[1]):.2f} dólares'
            crypto_str_final += crypto_str
        else:
            crypto_str = f'{x[0]}: ${float(x[1]):.2f} dólares \n'
            crypto_str_final += crypto_str
    return crypto_str_final

def variacao_bitcoin():
    porc = (crypto_price('bitcoin') - database.get_last_bitcoin_price())/crypto_price('bitcoin')*100
    #Dividi em 2 pq n consegui retornar com o sinal da operação.
    if porc > 0:
        porc = f'+{porc:.2f}%'
    else:
        porc = f'{porc:.2f}%'
    return porc
