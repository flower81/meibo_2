from flask import Flask, render_template, request #追加
import MySQLdb #追加

app = Flask(__name__)

conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='10baton',
        db='meibo_db',
        charset='utf8',
    )
curs = conn.cursor()    #   mysqlと接続する時に使う


@app.route('/', methods=['POST','GET'])
def hello():
    kekka = ''      #   検索結果を格納する変数
    p = "'"     #   「'」を格納する変数
    jokenlst = ['id','lastname','firstname','lstyomi','fstyomi','start','startTo','birth','birthTo','age','ageTo']
    #   検索条件をリスト化
    glNgs = 0   #   GETした検索語句リスト(getlst)の長さ(要素数)を格納する変数
    dic = {}    #   検索語句と検索条件を結び辞書型にし、格納する変数
    bns = ''    #   文章(sql文の後半)を格納する変数
    wrdA = ' AND '  #   見た通り


    if request.method == 'POST':
        getlst = request.form.getlist('sagasu') #   入力された検索語句をリスト型として取得
        print(getlst)
        glNgs = len(getlst) #   getlstの長さ(要素数)を格納
        for i in range(glNgs):  #   glNgs回処理を繰り返す
            w = getlst[i]   #   wにはgetlst(検索語句)が順に格納される
            nn = jokenlst[i]    #   nnにはjokenlst(検索条件)が順に格納される
            dic[w] = nn     #   {キー:値}={検索語句:検索条件}={w:nn}という辞書型になる
        list02 = [i for i, i in enumerate(getlst) if i != '']
        #   list02はgetlst(検索語句)の空白ではないリスト型を生成
        lst2ngs = len(list02)   #   list02の長さ(要素数)を格納

        if lst2ngs > 1:
            if getlst[5] != '' and getlst[6] != '':
                sql = "SELECT * FROM meibotest WHERE " + str(jokenlst[5]) + ' between ' + p + str(getlst[5]) + p + ' and ' + p + str(getlst[6]) + p

            elif getlst[7] != '' and getlst[8] != '':
                sql = "SELECT * FROM meibotest WHERE " + str(jokenlst[7]) + ' between ' + p + str(getlst[7]) + p + ' and ' + p + str(getlst[8]) + p

            elif getlst[9] != '' and getlst[10] != '':
                sql = "SELECT * FROM meibotest WHERE " + str(jokenlst[9]) + ' between ' + p + str(getlst[9]) + p + ' and ' + p + str(getlst[10]) + p

            else:
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
        getlst = None

    #return name
    return render_template('hello.html',
                            title='flask test',
                            kekka=kekka
                            ) #変更

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/add',methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        addlist = request.form.getlist('tsuika') #   入力された検索語句をリスト型として取得
        print(addlist)
#        print('test')
    else:
        addlist = 'no list'
        print(addlist)
    return render_template('add.html')

@app.route('/add_check')
def add_check():
    if request.method == 'POST':
        addlist = request.form.getlist('tsuika')
        print(addlist)
    else:
        addlist = 'no list'
    return render_template('add_check.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')



## おまじない
if __name__ == "__main__":
    app.run(debug=True)
