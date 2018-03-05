from flask import Flask, render_template, request #追加
import MySQLdb #追加
from slackclient import SlackClient

app = Flask(__name__)

conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='10baton',
        db='meibo_db',
        charset='utf8',
    )

def post_slack(message):
    token = "xoxb-270694051571-0t6GZJ0j0uBgaN62Kgt1ey42"
    sc = SlackClient(token)
    sc.api_call(
        "chat.postMessage",
        channel="#test_pair",
        text=message,
        username='meibo.',
        icon_emoji=':robot_face:'
    )


curs = conn.cursor()    #   mysqlと接続する時に使う
addlist = []
p = "'"     #   「'」を格納する変数
getid = ''
upid = ''
result = ''
upcon = []
dic = {}
dic_check = {}    #   検索語句と検索条件を結び辞書型にし、格納する変数
dic_com = {}

@app.route('/', methods=['POST','GET'])
def hello():
    jokenlst = ['id','lastname','firstname','lstyomi','fstyomi','start','startTo','birth','birthTo','age','ageTo']
    #   検索条件をリスト化
    kekka = ''      #   検索結果を格納する変数
    glNgs = 0   #   GETした検索語句リスト(getlst)の長さ(要素数)を格納する変数
    bns = ''    #   文章(sql文の後半)を格納する変数
    wrdA = ' AND '  #   見た通り

    conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='10baton',
            db='meibo_db',
            charset='utf8',
        )

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

#@app.route('/add',methods=['POST', 'GET'])
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/add_check', methods=['POST','GET'])
def add_check():
    if request.method == 'POST':
        global addlist
        addlist = request.form.getlist('tsuika')
        print(addlist)

    else:
        addlist = 'no list'
        print(addlist)

    return render_template('add_check.html', addlist=addlist)

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/update_check', methods=['POST','GET'])
def update_check():
    result= ''
    miss = ''
    if request.method == 'POST':
        global upid
        upid = request.form['shusei']
        sql = "SELECT * FROM meibotest WHERE id = " + p + str(upid) + p

        try:
            curs.execute(sql)
            result = curs.fetchall()
            for id, lastname, firstname, lstyomi, fstyomi, start, birth, age in result:
                print(id, lastname, firstname, lstyomi, fstyomi, start, birth, age)
        except:
            print('sql動作は失敗しました')

    else:
        upid = None
    return render_template('update_check.html', result=result, miss=miss)

@app.route('/last_check', methods=['POST','GET'])
def last_check():
    jokenlst = ['id','lastname','firstname','lstyomi','fstyomi','start','birth','age']
    if request.method == 'POST':
        global upcon
        upcon = request.form.getlist('kosin')
        print(upcon)
        sql = "SELECT * FROM meibotest WHERE id = " + p + str(upid) + p
        try:
            curs.execute(sql)
            result = curs.fetchall()
        except:
            print('sql動作は失敗しました')
        ucNgs = len(upcon)
        print('チェック　', upcon)
        for i in range(ucNgs):
            w = upcon[i]
            nn = jokenlst[i]
            global dic_check
            dic_check[nn] = w

        for i in range(ucNgs):
            w = upcon[i]
            nn = jokenlst[i]
            global dic_com
            dic_com[w] = nn

        print(dic_check)
        print(dic_com)

    else:
        upcon = None

    return render_template('last_check.html', upcon=upcon, result=result, dic_check=dic_check)

@app.route('/delete')
def delete():
    return render_template('delete.html')

#@app.route('/delete_check')
@app.route('/delete_check', methods=['POST'])
def delete_check():
    if request.method == 'POST':
        global getid
        getid = request.form['sakujo']
        print(getid)

        sql = "SELECT * FROM meibotest WHERE id = " + p + str(getid) + p
        print(sql)

        curs.execute(sql)
        result = curs.fetchall()

        for id, lastname, firstname, lstyomi, fstyomi, start, birth, age in result:
            print(id, lastname, firstname, lstyomi, fstyomi, start, birth, age)

    return render_template('delete_check.html', result=result)

@app.route('/complete')
def complete():
    sql = ''
    p = "'"
    sentence = ''
    num = 0
    if addlist != []:
        sql = 'INSERT INTO meibotest (id, lastname, firstname, lstyomi, fstyomi, start, birth, age) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(addlist[0], addlist[1], addlist[2], addlist[3], addlist[4], addlist[5], addlist[6], addlist[7])
        word0 = p + str(addlist[0]) + p
        word1 = p + str(addlist[1]) + p
        word2 = p + str(addlist[2]) + p
        word3 = p + str(addlist[3]) + p
        word4 = p + str(addlist[4]) + p
        word5 = p + str(addlist[5]) + p
        word6 = p + str(addlist[6]) + p
        word7 = p + str(addlist[7]) + p

        sql = 'INSERT INTO meibotest (id, lastname, firstname, lstyomi, fstyomi, start, birth, age) VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})'.format(word0, word1, word2, word3, word4, word5, word6, word7)
        print(sql)
        curs.execute(sql)
        conn.commit()
        conn.close()
        post_slack('追加したよ')

    elif getid != '':
        dltsql = 'DELETE FROM meibotest WHERE id = ' + p + getid + p

        curs.execute(dltsql)
        conn.commit()
        print(str(getid) + 'を削除しました。')

    elif upcon != []:
        print('たどり着いた', dic_com)
        list02 = [i for i, i in enumerate(upcon) if i != '']
        print(list02)

        for j in list02:
            sentence += str(dic_com[j]) + ' = ' + p + str(list02[num]) + p + ', '
            num += 1
        sentence = sentence.rstrip(', ')
        print(sentence)
        sql = "UPDATE meibotest SET " + sentence + " WHERE id = " + str(upid)
        print(sql)

        try:
            curs.execute(sql)
            conn.commit()
        except:
            print('sql失敗しました')
            print('実行したsql文は', sql, 'です')

    else:
        print('失敗しました')

    return render_template('complete.html')

## おまじない
if __name__ == "__main__":
    app.run(debug=True)
