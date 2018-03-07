#   coding: utf-8
import MySQLdb #追加

conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='10baton',
        db='meibo_db',
        charset='utf8',
    )

curs = conn.cursor()    #   mysqlと接続する時に使う


sentence = input('=> ')
sentence2 = input('==> ')

sql = "SELECT * FROM meibotest WHERE lastname LIKE " + "'%" + sentence + "%'" + " OR lastname LIKE " + "'%" + sentence2 + "%'"

curs.execute(sql)
result = curs.fetchall()

for id, lastname, firstname, lstyomi, fstyomi, start, birth, age in result:
    print(id, lastname, firstname, lstyomi, fstyomi, start, birth, age)
