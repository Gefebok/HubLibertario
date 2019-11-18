from database import add_crypto_db
from ancapball import ancapball_comparison
from noticias import boletim_bitcoin
import datetime

def get_daily_posts():
    f_read = open('ancapball_today.txt', 'r')
    hoje = int(f_read.read().strip())
    f_read.close()
    return hoje
def set_daily_posts(today):
    f_write = open('ancapball_today.txt', 'w')
    f_write.write(str(today))
    f_write.close()
    return
def daily_posts():
    today = datetime.datetime.now ()
    hour = today.strftime('%H')
    if int(hour) == 13:
        if get_daily_posts() == 0:
            ancapball_comparison()
            set_daily_posts(1)
    elif int(hour) == 19:
        if get_daily_posts() == 1:
            boletim_bitcoin()
            set_daily_posts(2)
            add_crypto_db('bitcoin')
    elif int(hour) == 0:
        if get_daily_posts() == 2:
            set_daily_posts(0)
    return
