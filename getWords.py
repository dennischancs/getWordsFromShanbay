# 导入库
import sys
import io
import time
import json
import requests
from requests.cookies import RequestsCookieJar
import bs4

# 存储 JSON 文件
def saveJSON(data, filename):
    print('存储数据', filename, '中...')
    with open('./data/' + filename + '.json', 'w') as fileObject:
        json.dump(data, fileObject)

# 读取 JSON 文件
def loadJSON(filename):
    print('读取数据', filename, '中...')
    with open('./data/' + filename + '.json', 'r') as fileObject:
        data = json.load(fileObject)
        return data


# 可以手动预设 categories
# 比如已爬取到 wordlist，之后爬取 words，不用从头再来，可以直接写成这样：
# categories = [] # 从重新爬取
categories = loadJSON('wordlist') # 但2020/02/06测试时，单词书连接已经失效，只能利用原wordlist

# 设置需要爬取的单词书类别 category 和数量 count
selectBooks = [
    {'category': '考研', 'count': '40'},
    {'category': '托福', 'count': '29'},
    {'category': '雅思', 'count': '45'},
    {'category': 'GRE', 'count': '10'},
    {'category': '四级', 'count': '22'},
    {'category': '六级', 'count': '13'},
    {'category': 'BEC', 'count': '8'},
    {'category': '英专', 'count': '19'},
    {'category': '托业', 'count': '6'},
    {'category': 'GMAT', 'count': '5'},
    {'category': 'SAT', 'count': '17'},
    {'category': 'ACT', 'count': '1'},
    {'category': '高中', 'count': '83'},
    {'category': '初中', 'count': '87'},
    {'category': '小学', 'count': '112'},
    {'category': '医学', 'count': '38'},
    {'category': '计算机', 'count': '16'},
    {'category': '文学作品', 'count': '33'},
    {'category': '英语辅导', 'count': '39'},
    {'category': '公共英语', 'count': '36'},
    {'category': '公开课', 'count': '9'},
    {'category': '影视剧', 'count': '34'},
    {'category': '其他', 'count': '137'}
]

# 模拟登录
# [Python3.6下的Requests登录及利用Cookies登录 - 西柳居士 - 博客园](https://www.cnblogs.com/ddddfpxx/p/8624715.html)

# 预设 url
urls = {
    'base': 'https://www.shanbay.com/',
    'login': 'https://apiv3.shanbay.com/bayuser/login',
    'cookies_login': 'https://apiv3.shanbay.com/uc/checkin?_=', # 用已有Cookies登陆,GET方法, '='后面的数字是毫秒时间戳(13位数字)
    'categories': 'https://www.shanbay.com/wordbook/books/mine/',
    'category': 'https://www.shanbay.com/wordbook/category/'
}

# 预设 header
headers = {
    'Host': 'apiv3.shanbay.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Origin': 'https://www.shanbay.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.shanbay.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5,ja;q=0.4,de-DE;q=0.3,de;q=0.2,zh-TW;q=0.1,und;q=0.1'
}
# 填写登陆后的浏览器cookies
cookies = {
    'csrftoken': 'DA9Is2Et4jnSMo****URI5lyvvBnxOD',
    '_ga': 'GA1.2.1767870350.1580901205',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22tlsyvn%22%2C%22first_id%22%3A%2217015103c6d1e6-025c894ac78401-b383f66-1327104-17015103c6e648%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22%24device_id%22%3A%2217015103c6d1e6-025c894ac78401-b383f66-1327104-17015103c6e648%22%7D',
    'sessionid': '"e30:1izPFD:FtbuI-pzlSu99oTUUgucx7kQhoo"',
    'auth_token': 'eyJ0eXAiOiJKV1****ciOiJIUzI1NiJ9.eyJpZCI6NTY2Njc3ODcsImV4cCI6MTU4MTc5MDk3OSwiZGV2aWNlIjoiIiwidXNlcm5hbWUiOiJEZW5uaXNfQ2hhbiIsImlzX3N0YWZmIjowfQ.4XMRFlsFJ9rL4CaF6_jHDBpKPCN3FOZAu4hTGbNSPx4'
}

# 由于本人不会模拟滑动验证码，暂时采用Cookies登陆(Cookies有效期10天)
def login():
    r = s.get(urls['cookies_login']+str(round(time.time() * 1000)), headers=headers, cookies=cookies, verify=False)
    print('登录状态 ', r.status_code)

# 创建 session
s = requests.session()
print('建立连接 ')

# # 爬取单词书类目
# def getCategories():
#     r = s.get(urls['categories'], headers=headers['base'])
#     print('单词书类别 ', r.status_code)
#     print('开始解析')
#     soup = bs4.BeautifulSoup(r.text, features='lxml')
#     tags_li = soup.find(id='wordbook-category-list').find_all('li')
#     for tag_li in tags_li:
#         data = tag_li['data']
#         category = tag_li.text
#         categories.append({'id': data, 'category': category})
#     print('完成解析')
#     saveJSON(categories, 'categories')

# # 爬取单词书列表
# def getWordbooks():
#     for category in categories:
#         r = s.get(urls['category'] + category['id'])
#         soup = bs4.BeautifulSoup(r.text, features='lxml')
#         tags_book = soup.find_all(class_='wordbook-title')
#         category['wordbooks'] = []
#         for tag_book in tags_book:
#             title = tag_book.text
#             href = tag_book.find('a')['href']
#             category['wordbooks'].append({'title': title, 'href': href})
#     saveJSON(categories, 'wordbooks')

# 爬取单词列表
# def getWordlist():
#     for category in categories:
#         for wordbook in category['wordbooks']:
#             r = s.get(urls['base'] + wordbook['href'])
#             soup = bs4.BeautifulSoup(r.text, features='lxml')
#             tags_worditem = soup.find_all(class_='wordbook-wordlist-name')
#             tags_wordcount = soup.find_all(class_='wordbook-wordlist-count')
#             print(tags_worditem)
#             wordbook['wordlist'] = []
#             for i in range(len(tags_worditem)):
#                 title = tags_worditem[i].text
#                 href = tags_worditem[i].find('a')['href']
#                 count = tags_wordcount[i].text
#                 print(title, href, count)
#                 wordbook['wordlist'].append(
#                     {'title': title, 'href': href, 'count': count})
#     saveJSON(categories, 'wordlist')

# 爬取单词
def getWords(selectBooks):
    words = []
    for select in selectBooks:
        category = select['category']
        countMax = int(select['count'])
        countNow = 0
        words.append({'category': category, 'wordbooks': []})
        for category_ in categories:
            if (category_['category'] == category):
                for wordbook in category_['wordbooks']:
                    if (countNow >= countMax):
                        break
                    countNow += 1
                    words[-1]['wordbooks'].append(
                        {'title': wordbook['title'], 'words': []})
                    for wordlist in wordbook['wordlist']:
                        for page in range(11):  # 最多 10 页
                            time.sleep(0.25) #控制爬虫速度
                            print(category_['category'],
                                  wordbook['title'], wordlist['title'], '  #', page)
                            r = s.get(urls['base'] + wordlist['href'],
                                      params={'page': str(page)})
                            soup = bs4.BeautifulSoup(r.text, features='lxml')
                            tag_main = soup.find(class_='main-body')
                            tags_word_en = tag_main.find_all(class_='span2')
                            tags_word_zh = tag_main.find_all(class_='span10')
                            for i in range(len(tags_word_en)):
                                en = tags_word_en[i].text
                                zh = tags_word_zh[i].text
                                words[-1]['wordbooks'][-1]['words'].append(
                                    {'en': en, 'zh': zh})
                    saveJSON(words, 'wordsSelected_tmp') # 临时存储，总是截至最近的那本书
    saveJSON(words, 'wordsSelected') # 汇总


# 开始执行
if __name__ == '__main__':
    login()
    # getCategories()
    # getWordbooks()
    # getWordlist()
    getWords(selectBooks)
