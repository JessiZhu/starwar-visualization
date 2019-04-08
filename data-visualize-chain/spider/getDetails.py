
import urllib
import urllib.request
from bs4 import BeautifulSoup

fr = open('douban_movie.txt','r' , encoding='utf8')
fw = open('douban_movie_detail.txt' , 'w' ,encoding='utf8')

fw.write('id^title^url^cover^rate^director^composer^actor^category^district^language^showtime^length^othername^description\n')

count = 1
firstline = True

for line in fr:
    if firstline:
        firstline = False
        continue
    line = line.split(';')
    movieId = line[0]
    title = line[1]
    url = line[2]
    cover = line[3]
    rate = line[4].rstrip('\n')

    response = urllib.request.urlopen(url=url)
    html = response.read()
    html = BeautifulSoup(html , 'html.parser')

    info = html.select('#info')[0]

    info = info.get_text().split('\n')
    print(str(count) + ' '+ str(len(info)) + ' '+ title)
    # for item in info:
    #     print(item)
    if len(info) == 13:
        director = info[1].split(':')[-1].strip()
        composer = info[2].split(':')[-1].strip()
        actor = info[3].split(':')[-1].strip()
        category = info[4].split(':')[-1].strip()
        district = info[6].split(':')[-1].strip()
        language = info[7].split(':')[-1].strip()
        showtime = info[8].split(':')[-1].strip()
        length = info[9].split(':')[-1].strip()
        othername = info[10].split(':')[-1].strip()
    elif len(info) == 12:
        director = info[1].split(':')[-1].strip()
        composer = info[2].split(':')[-1].strip()
        actor = info[3].split(':')[-1].strip()
        category = info[4].split(':')[-1].strip()
        district = info[5].split(':')[-1].strip()
        language = info[6].split(':')[-1].strip()
        showtime = info[7].split(':')[-1].strip()
        length = info[8].split(':')[-1].strip()
        othername = info[9].split(':')[-1].strip()
    else:
        continue
    description = html.find_all('span' , attrs={"property": "v:summary"})[0].get_text().strip()
    description = description.lstrip().lstrip('\n\t').rstrip().rstrip('\n\t').replace('\n', '\t')

    record = str(movieId) +'^'+ title +'^'+ url +'^'+ cover +'^'+ str(rate) +'^'+ director +'^'+ composer +'^'+ actor +'^'+ category +'^'+ district +'^'+ language +'^'+ str(showtime) +'^'+ str(length) +'^'+ othername +'^'+ description+'\n'
    fw.write(record)

    count = count + 1

fr.close()
fw.close()




