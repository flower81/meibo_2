from flask import Flask, render_template, request #追加
import MySQLdb #追加

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
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
    sql = "select * from meibotest"
    curs.execute(sql)
    members = curs.fetchall()

    curs.close()
    conn.close()

    try:
        value_search = request.form['search']

        prType = type(value_search)
        print(prType)

    except:
        value_search = None


    #return name
    return render_template('hello.html',
                            title='flask test',
                            members=members,
                            value_search=value_search) #変更

## おまじない
if __name__ == "__main__":
    app.run(debug=True)
