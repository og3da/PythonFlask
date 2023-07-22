import sqlite3

conecction = sqlite3.connect('banco.db')
cursor = conecction.cursor()

cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY,\
 nome text, estrelas real, diaria real, cidade text)"

cria_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Alpha hotel', 4.5, 420.1, 'Rio de janeiro')"

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)

conecction.commit()
conecction.close()