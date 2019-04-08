from flask import *
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)


def connectdb():
    db = MySQLdb.connect(host = 'localhost' , user = 'root' , password = '' , db = 'douban' , port = 3306 , charset = 'utf8' , cursorclass = MySQLdb.cursors.DictCursor)
    db.autocommit(True)
    cursor = db.cursor()
    return db , cursor

def closedb(db , cursor):
    cursor.close()
    db.close()

@app.route('/')
def index():
    (db ,cursor) = connectdb()
    cursor.execute('select * from moives')
    movies = cursor.fetchall()
    app.logger.info('shdfiosdf')
    closedb(db , cursor)
    return render_template('index.html')

@app.route('/rate')
def rate():
    return render_template('rate.html')

@app.route('/search')
def search():
    return render_template('search.html')
if __name__ == '__main__':
    app.run(debug=True)
