
import MySQLdb
import MySQLdb.cursors

fr = open('douban_movie_clean.txt' , 'r' , encoding='utf8')
db = MySQLdb.connect(host='localhost', user='root', passwd='', db='douban', port=3306, charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
db.autocommit(True)
cursor = db.cursor()

categories = {}

districts = {}

languages = {}

showtimes = {}

lengths = {}

rates = {}

combined = {}

isFirstLine = True

for line in fr:
    if isFirstLine:
        isFirstLine = False
        continue

    line = line.split('^')

    # 统计各个区域各个分类的平均评分
    district = line[9].split('/')
    category = line[8].split('/')
    rate = float(line[4])
    for d in district:
        d = d.split('_')[0]
        if d not in combined.keys():
            combined[d] = {}
        for c in category:
            if c == '':
                continue
            if c not in combined[d].keys():
                combined[d][c] = {'average':0.0 , 'count':0.0}
            combined[d][c]['average'] = (combined[d][c]['average'] * combined[d][c]['count'] + rate)/(combined[d][c]['count'] + 1)
            combined[d][c]['count'] = combined[d][c]['count'] + 1

    # 分类统计
    category = line[8].split('/')
    for c in category:
        if c == '':
            continue
        if c not in categories.keys():
            categories[c] = 1
        else:
            categories[c] = categories[c] + 1

    # 区域统计
    district = line[9].split('/')
    for d in district:
        d = d.split('_')
        if d[0] == '':
            continue
        if d[0] not in districts.keys():
            districts[d[0]] = 1
        else:
            districts[d[0]] = districts[d] + 1

    # 语言统计
    language = line[10].split('/')
    for item in language:
        if item == '':
            continue
        if item not in languages.keys():
            languages[item] = 1
        else:
            languages[item] = languages[item] + 1

    # 上映时间统计
    showtime = line[11]
    if not showtime == '':
        if showtime not in showtimes.keys():
            showtimes[showtime] = 1
        else:
            showtimes[showtime] = showtimes[showtime] + 1

    # 片长统计
    length = line[12]
    if not length == '':
        if length not in lengths.keys():
            lengths['length'] = 1
        else:
            lengths['length'] = lengths['length'] + 1

    # 评分统计\
    rate = line[4]
    if not rate == '':
        if rate not in rates.keys():
            rates['rate'] = 1
        else:
            rates['rate'] = rates['rate'] + 1

    temp = {}
    for key, value in combined.items():
        print(key + ' ' + str(value))
        temp[key] = {}
        temp1 = ''
        temp2 = ''
        for k, v in value.items():
            print(k + ' ' + str(v))
            temp1 = temp1 + k + ','
            temp2 = temp2 + '%.1f' % v['average'] + ','
        temp[key]['categories'] = temp1[:-1]
        temp[key]['rates'] = temp2[:-1]
        print(key +' '+ temp1[:-1] +' '+ temp2[:-1])
        cursor.execute("insert into rate(name,categories,rates) values(%s,%s,%s)", [key, temp1[:-1], temp2[:-1]])

fr.close()
cursor.close()
db.close()