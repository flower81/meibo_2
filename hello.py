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

    curs = conn.cursor()    #   mysqlと接続する時に使う
    kekka = ''      #   検索結果を格納する変数
    p = "'"     #   「'」を格納する変数
    jokenlst = ['id','lastname','firstname','lstyomi','fstyomi','start','birth','age']
    #   検索条件をリスト化
    glNgs = 0   #   GETした検索語句リスト(getlst)の長さ(要素数)を格納する変数
    dic = {}    #   検索語句と検索条件を結び辞書型にし、格納する変数
    bns = ''    #   文章(sql文の後半)を格納する変数
    wrdA = ' AND '  #   見た通り

    
    if request.method == 'POST':
        getlst = request.form.getlist('sagasu')
        print(getlst)
        glNgs = len(getlst)
        for i in range(glNgs):
            w = getlst[i]
            nn = jokenlst[i]
            dic[w] = nn
        print(dic)
        list02 = [i for i, i in enumerate(getlst) if i != '']
        lst2ngs = len(list02)

        if lst2ngs > 1:
            for j in list02:
                bns += str(dic[j]) + ' = ' + p + j + p + wrdA
            bns = bns.rstrip(' AND ')
            sql = "SELECT * FROM meibotest WHERE " + bns

        elif lst2ngs == 1:
            for j in list02:
                bns += str(dic[j]) + ' = ' + p + j + p + wrdA
            bns = bns.rstrip(' AND ')
            sql = "SELECT * FROM meibotest WHERE " + bns

        elif lst2ngs == 0:
            sql = ("SELECT * FROM meibotest")

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
