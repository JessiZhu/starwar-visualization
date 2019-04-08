from flask import *
import MySQLdb
import MySQLdb.cursors
from config import *
import time

app = Flask(__name__)

def connectdb():
    db = MySQLdb.connect(host = HOST , user = USER , password = PASSWORD , port = PORT ,
                         db = DATABASE , charset = CHARSET , cursorclass = MySQLdb.cursors.DictCursor )
    db.autocommit(True)
    cursor =db.cursor()
    return db , cursor

def closedb(db , cursor):
    db.close()
    cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle' , methods=['post'])
def handle():
    data = request.form
    (db , cursor) = connectdb()
    cursor.execute("insert into post(title, content, timestamp) values(%s, %s, %s)", [data['title'], data['content'], str(int(time.time()))])
    post_id = cursor.lastrowid
    # closedb(db , cursor)
    return redirect(url_for('post' , post_id = post_id))

@app.route('/list')
def list():
    (db , cursor) = connectdb()
    cursor.execute("select * from post")
    posts = cursor.fetchall()
    for x in range(0 , len(posts)):
        posts[x]['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(posts[x]['timestamp'])))
    return render_template('list.html' , posts = posts)

@app.route('/post/<post_id>')
def post(post_id):
    (db , cursor) = connectdb()
    cursor.execute("select * from post where id=%s" ,[post_id])
    post = cursor.fetchone()
    post['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(post['timestamp'])))
    # closedb(db , cursor)
    return render_template('post.html' , post = post)

if __name__ == '__main__':
    app.run(debug=True)

app.config.from_object(__name__)

