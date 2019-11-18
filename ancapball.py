from database import add_ancapball_db, get_last_ancapball_followers
import datetime
from API_Twitter import api

def ancapball_comparison():
    id_ancapball = api.get_user('@ancapball_br')
    ancapball_ontem = get_last_ancapball_followers()
    ancapball_last = int(id_ancapball.followers_count)
    today = datetime.datetime.now()
    n_day = today.strftime('%j')
    initial_day = 312
    print(f'Ancapball esta agora com {ancapball_last} seguidores, {ancapball_last - ancapball_ontem} a mais do que ontem.')
    print(f'Faz {int(n_day) - initial_day} dias da decisao do STF, desde entao ancapball ganhou {ancapball_last - 20632} seguidores!')
    api.update_status(f'Faz {int(n_day) - initial_day} dias desde a decisão do STF sobre prisão em segunda instancia, '
                      f'desde então a @ancapball_br ganhou {ancapball_last - 20632} seguidores!'
                      f' {ancapball_last - ancapball_ontem} a mais que ontem, contabilizando {ancapball_last} seguidores!')
    try:
        add_ancapball_db(ancapball_last)
        return
    except:
        return
