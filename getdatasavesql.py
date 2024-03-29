# =============================================================================
# 爬数入库(mysql)
# =============================================================================

import requests
import re
import pymysql

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}


def baidu(company):
    url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + company
    res = requests.get(url, headers=headers).text

    # 正则表达式编写
    p_info = '<p class="c-author">(.*?)</p>'
    info = re.findall(p_info, res, re.S)
    p_href = '<h3 class="c-title">.*?<a href="(.*?)"'
    href = re.findall(p_href, res, re.S)
    p_title = '<h3 class="c-title">.*?>(.*?)</a>'
    title = re.findall(p_title, res, re.S)

    # 数据清洗
    source = []  # 先创建两个空列表来储存等会分割后的来源和日期
    date = []
    for i in range(len(info)):
        title[i] = title[i].strip()
        title[i] = re.sub('<.*?>', '', title[i])
        info[i] = re.sub('<.*?>', '', info[i])
        source.append(info[i].split('&nbsp;&nbsp;')[0])
        date.append(info[i].split('&nbsp;&nbsp;')[1])
        source[i] = source[i].strip()
        date[i] = date[i].strip()
        print(str(i + 1) + '.' + title[i] + '(' + date[i] + '-' + source[i] + ')')
        print(href[i])

    # 将数据存入数据库
    for i in range(len(title)):
        db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='financedatahub', charset='utf8')
        cur = db.cursor()
        sql = 'INSERT INTO test(company,title,href,source,date) VALUES (%s,%s,%s,%s,%s)'
        cur.execute(sql, (company, title[i], href[i], source[i], date[i]))
        db.commit()
        cur.close()
        db.close()


baidu('阿里巴巴')
print('数据爬取并存入数据库成功')

# 如果想批量爬取并存入数据库，可以采用如下代码：
companys = ['华泰证券', '阿里巴巴', 'TCL集团', '上海贝岭', '长江电力']
for company in companys:  
    try:
        baidu(company)
        print(company + '爬取并存入数据库成功')
    except:
        print(company + '爬取并存入数据库失败')
