import MySQLdb
import MySQLdb.cursors

fr = open('douban_movie_clean.txt', 'r' ,encoding='utf8')

db = MySQLdb.connect(host = 'localhost' , user = 'root' , password = '' , db = 'douban' , port = 3306 , cursorclass = MySQLdb.cursors.DictCursor , charset = 'utf8')
db.autocommit(True)
cursor = db.cursor()

count = 0
isFirstLine = True

for line in fr:
    if isFirstLine:
        isFirstLine = False
        continue

    line = line.split('^')

    movieId = line[0]
    title = line[1]
    url = line[2]
    cover = line[3]
    rate = line[4]
    director = line[5]
    composer = line[6]
    actor = line[7]
    category = line[8]
    district = line[9]
    language = line[10]
    showtime = line[11]
    length = line[12]
    othername = line[13]
    description = line[14]

    cursor.execute('insert into moives(movieId,title,url,cover,rate,director,composer,actor,category,district,language,showtime,length,othername,description) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[movieId,title,url,cover,rate,director,composer,actor,category,district,language,showtime,length,othername,description])

    count = count + 1

fr.close()

cursor.close()










