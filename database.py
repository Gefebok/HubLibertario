import datetime
import pymysql
import cryptos

db = pymysql.connect ('localhost', 'USUARIO', 'SENHA', 'NOME_DB')

cursor = db.cursor ()
##----------------------------------------CRYPTOS-----------------------------------------##
cryptos_monitoradas = ('bitcoin')
def add_crypto_db(crypto):
    if crypto in cryptos_monitoradas:
        hoje = datetime.date.today ()
        hoje = hoje.strftime('%Y%m%d') #É necesário usar o strftime pois o DATE do SQL é em ano, mês e dia (com ano não sendo abreviado)
        crypto_preco = cryptos.crypto_price(crypto)
        cursor.execute(f'INSERT INTO `{crypto}`(`preco`, `dia`) VALUES ({crypto_preco}, {hoje})') #Comando SQL,
        print(crypto_preco)
    else:
        return print('Nao tem essa crypto')
    db.close()

def get_last_bitcoin_price():
    ontem = datetime.datetime.today()-datetime.timedelta(days=1)
    ontem = ontem.strftime('%Y%m%d')
    try:
        cursor.execute(f'SELECT preco FROM bitcoin WHERE dia = {ontem}')
        results = cursor.fetchall()
        return results[0][0]
    except:
        db.rollback()
    db.close()
##----------------------------------------CRYPTOS-----------------------------------------##

##----------------------------------------ANCAPBAL----------------------------------------##
def add_ancapball_db(seguidores):
    hoje = datetime.date.today ()
    hoje = hoje.strftime ('%Y%m%d')
    try:
        cursor.execute(f'INSERT INTO `ancapball` VALUES({hoje}, {seguidores})')
    except:
        db.rollback()
def get_last_ancapball_followers():
    ontem = datetime.date.today () - datetime.timedelta (days=1)
    ontem = ontem.strftime ('%Y%m%d')
    try:
        cursor.execute(f'SELECT Seguidores FROM ancapball WHERE Data = {ontem}')
        results = cursor.fetchall()
        return results[0][0]
    except:
        db.rollback()
    db.close()
##----------------------------------------ANCAPBAL----------------------------------------##

##----------------------------------------USUARIOS----------------------------------------##
def check_user_db(id):
    cursor.execute (f'SELECT usuario FROM users')
    results = cursor.fetchall()
    for x in results:
        if x[0] == id:
            return True
        else:
            continue
    add_user_db(id)

def add_user_db(usuario):
    from random import randint
    cursor.execute(f'INSERT INTO `users` VALUES("{usuario}", {randint(0,100)}, {randint(0,100)}, {randint(0,100)})')

def get_user(id, porc):
    cursor.execute (f'SELECT {porc} from users WHERE usuario = "{id}"')
    results = cursor.fetchall()
    return results[0][0]
##----------------------------------------USUARIOS----------------------------------------##
def retweet_autentication():
    cursor.execute(f'SELECT id FROM retweet')
    results = cursor.fetchall()
    return results
