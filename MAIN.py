from API_Twitter import api
from time import sleep
from cryptos import crypto_price
from dailys import daily_posts
from database import check_user_db, get_user, retweet_autentication

mentions = api.mentions_timeline()
FILE_NAME = "last_seen_id.txt"

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
def analise():
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
        since_id=last_seen_id,
        tweet_mode='extended')
    cryptos = [['#bitcoin', 'do Bitcoin', 'bitcoin'], ['#ethereum', 'do Ethereum', 'ethereum'],
               ['#nano', 'da Nano', 'nano'],['#litecoin', 'da Litecoin', 'litecoin'],
               ['#monero', 'do Monero', 'monero'], ['#dash', 'da Dash', 'dash']]

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id,FILE_NAME)
        porc = (('#soça', 'soca', 'soça'), ('#fascista', 'fascista', 'fascista'), ('#ancap', 'ancap', 'ancap'), ('#comunista', 'soca', 'comunista'))
        #Analise de #
        if '#retweet' in mention.full_text.lower():
            autenticado = False
            for x in retweet_autentication():
                if mention.user.screen_name in x[0]:
                    autenticado = True
            if autenticado == True:
                reply_id = api.get_status (mention.id).in_reply_to_status_id
                api.retweet(reply_id)
            else:
                api.send_direct_message (mention.user.id, 'Voce nao tem permissao para usar o #retweet')
        elif '#crypto' in mention.full_text.lower():
            crypto_str = crypto_price('todos')
            crypto_str = crypto_str.strip()
            api.update_status('@' + mention.user.screen_name + '\n'
                f'{crypto_str}', mention.id)
        elif '#cripto' in mention.full_text.lower():
            crypto_str = crypto_price('todos')
            crypto_str = crypto_str.strip()
            api.update_status('@' + mention.user.screen_name + '\n'
                f'{crypto_str}', mention.id)
        else:
            for x in cryptos:
                if x[0] in mention.full_text.lower():
                    api.update_status('@' + mention.user.screen_name +
                                       f' O preço {x[1]} é: $' + f'{crypto_price(x[2]):.2f} dolares', mention.id)
            for x in porc:
                if x[0] in mention.full_text.lower():
                    check_user_db(mention.user.screen_name)
                    api.update_status('@' + mention.user.screen_name + '\n'
                    f'Voce é {get_user(mention.user.screen_name, x[1])}% {x[2]}!', mention.id)

while True:
    daily_posts()
    analise()
    sleep(15)
