import pymysql

db = pymysql.connect ('localhost', 'root', '', 'artigos')

cursor = db.cursor ()

def artigos_categorias():
    cursor.execute(f'SELECT table_name FROM information_schema.tables WHERE table_schema ="artigos"')
    results = cursor.fetchall()
    db.close()
    return results

def select_artigos(categoria):
    try:
        cursor.execute(f'SELECT * FROM {categoria}')
        results = cursor.fetchall()
        db.close()
        return results
    except:
        print('Nao ta funcionando')

for x in select_artigos('economia'):
    print('=-'*50 + '\n'
                    f'Nome: {x[0]}\n'
                    f'Autor: {x[4]}\n'
                    f'Descricao: {x[1]}\n'
                    f'Link: {x[2]}\n'
                    f'Audiobook: {x[3]}')
