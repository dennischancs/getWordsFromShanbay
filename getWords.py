# 导入库
import json
import requests
import bs4

# 可以手动预设 categories
# 比如已爬取到 wordlist，之后爬取 words，不用从头再来，可以直接写成这样：
# categories = loadJSON('wordlist)
categories = []

# 设置登录信息
userAccount = 'likeke'
userPassword = '123456'

# 设置需要爬取的单词书类别 category 和数量 count
selectBooks = [
    {'category': '四级', 'count': '5'},
    {'category': '六级', 'count': '3'},
    {'category': '考研', 'count': '2'}
]

# 模拟登录
def login():
    r = s.options(urls['login'], headers=headers['login1'])
    print('登录权限 ', r.status_code)
    r = s.post(urls['login'], headers=headers['login2'], json=datas['login'])
    print('登录状态 ', r.status_code)

# 爬取单词书类目
def getCategories():
    r = s.get(urls['categories'], headers=headers['base'])
    print('单词书类别 ', r.status_code)
    print('开始解析')
    soup = bs4.BeautifulSoup(r.text, features='lxml')
    tags_li = soup.find(id='wordbook-category-list').find_all('li')
    for tag_li in tags_li:
        data = tag_li['data']
        category = tag_li.text
        categories.append({'id': data, 'category': category})
    print('完成解析')
    saveJSON(categories, 'categories')

# 爬取单词书列表
def getWordbooks():
    for category in categories:
        r = s.get(urls['category'] + category['id'])
        soup = bs4.BeautifulSoup(r.text, features='lxml')
        tags_book = soup.find_all(class_='wordbook-title')
        category['wordbooks'] = []
        for tag_book in tags_book:
            title = tag_book.text
            href = tag_book.find('a')['href']
            category['wordbooks'].append({'title': title, 'href': href})
    saveJSON(categories, 'wordbooks')

# 爬取单词列表
def getWordlist():
    for category in categories:
        for wordbook in category['wordbooks']:
            r = s.get(urls['base'] + wordbook['href'])
            soup = bs4.BeautifulSoup(r.text, features='lxml')
            tags_worditem = soup.find_all(class_='wordbook-wordlist-name')
            tags_wordcount = soup.find_all(class_='wordbook-wordlist-count')
            print(tags_worditem)
            wordbook['wordlist'] = []
            for i in range(len(tags_worditem)):
                title = tags_worditem[i].text
                href = tags_worditem[i].find('a')['href']
                count = tags_wordcount[i].text
                print(title, href, count)
                wordbook['wordlist'].append(
                    {'title': title, 'href': href, 'count': count})
    saveJSON(categories, 'wordlist')

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
    saveJSON(words, 'wordsSelected')

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

# 预设 url
urls = {
    'base': 'https://www.shanbay.com/',
    'login': 'https://apiv3.shanbay.com/bayuser/login',
    'categories': 'https://www.shanbay.com/wordbook/books/mine/',
    'category': 'https://www.shanbay.com/wordbook/category/'

}

# 预设 header
headers = {
    'base': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    },
    'login1': {
        'Access-Control-Request-Headers': 'content-type,x-csrftoken',
        'Access-Control-Request-Method': 'POST',
        'Origin': 'https://web.shanbay.com',
        'Referer': 'https://web.shanbay.com/web/account/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    },
    'login2': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://web.shanbay.com',
        'Referer': 'https://web.shanbay.com/web/account/login',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-CSRFToken': '7USNYdUMVO1BVxGOAjSkFd88Liu9jvUY'
    }
}

# 预设 data
datas = {
    'login': {'account': userAccount, 'password': userPassword, 'code_2fa': ''}
}

# 创建 session
s = requests.session()
print('建立连接 ')

# 开始执行
if __name__ == '__main__':
    login()
    getCategories()
    getWordbooks()
    getWordlist()
    getWords(selectBooks)