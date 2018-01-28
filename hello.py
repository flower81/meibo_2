from flask import Flask, render_template, request #追加
import MySQLdb #追加

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def hello():
    #db setting
    conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='10baton',
            db='meibo_db',
            charset='utf8',
        )

    curs = conn.cursor()
    kekka = ''
    point = "'"

#    sql = "select * from meibotest"
#    curs.execute(sql)
#    members = curs.fetchall()

    #curs.close()
    #conn.close()

    if request.method == 'POST':
        value_search = request.form['sagasu']
        print('１段階')
        if value_search != "":
            check = 1
            print('２段階')
            if check == 1:
                sql = ("SELECT * FROM meibotest WHERE lastname = " + point + value_search + point)
            curs.execute(sql)
            kekka = curs.fetchall()

            for id, lastname, firstname, lstyomi, fstyomi, start, birth, age in kekka:
                print(id, lastname, firstname, lstyomi, fstyomi, start, birth, age)

    else:
        value_search = None

    #return name
    return render_template('hello.html',
                            title='flask test',
                            kekka=kekka
                            ) #変更

## おまじない
if __name__ == "__main__":
    app.run(debug=True)
