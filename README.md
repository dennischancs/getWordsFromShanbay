# 修改
参考：[likeke1997/getWordsFromShanbay](https://github.com/likeke1997/getWordsFromShanbay)

1. 改账号登陆为Cookies登陆；
2. 由于shanbay.com已更改单词书链接，但单词书的Lists链接没变，故依据[原项目2019-06提供的wordlist.json](https://github.com/likeke1997/getWordsFromShanbay)抓取了所有词表；
3. 完整爬取结果见`.\data\wordsSelected.json.7z`。

# 合并json
```python
json.dump([json.load(open('wordsSelected_11.json')), json.load(open('wordsSelected_12.json'))], open('wordsSelected_1.json','w'))
```

# 格式化json
```python
json_tmp = json.dumps(json.load(open('wordsSelected_1.json')), indent=4, sort_keys=False, ensure_ascii=False)
    with open('wordsSelected_1_fm.json', 'w') as json_file:
    json_file.write(json_tmp)
```

# 原说明
这是我用 Python 写的爬虫，能爬取扇贝网里的单词书和单词列表。使用到的库有`request`、`bs4`、`json`。

爬取结果展示（节选自`.\data\wordsSelected-example.json`）：

```json
[
  {
    "category": "四级",
    "wordbooks": [
      {
        "title": "\n2019四级真题核心词汇\n",
        "words": [
          {
            "en": "response",
            "zh": " n. 反应, 响应; 回答"
          },
          {
            "en": "lobby",
            "zh": " n. 大厅, 门廊, 门厅, 休息室, 游说议员者\nv. 游说"
          },
          {
            "en": "permission",
            "zh": " n. 同意,许可,允许"
          },
          {
            "en": "restraint",
            "zh": " n. 抑制,克制,束缚"
          },
          {
            "en": "restrict",
            "zh": " v. 限制,约束"
          },
        ...
```

# 使用

首先安装好代码依赖的库。

然后在`getWords.py`中配置如下信息：

```python
# 可以直接使用我爬取好的 wordlist
categories = loadJSON('wordlist')

# 填写登陆后的浏览器Cookies
cookies = {
    'csrftoken': 'AAAAAAAAAAAAAAAAAAAAAA',
    '_ga': 'AAAAAAAAAAAAAAAAAAAAAA5',
    'sensorsdata2015jssdkcross': 'AAAAAAAAAAAAAAAAAAAAAA',
    'sessionid': '"AAAAAAAAAAAAAAAAAAAAAA"',
    'auth_token': 'AAAAAAAAAAAAAAAAAAAAAA4'
}

# 配置需要爬取的单词书类别 category 和数量 count
selectBooks = [
    {'category': '四级', 'count': '5'},
    {'category': '六级', 'count': '3'},
    {'category': '考研', 'count': '2'}
]
```

然后打开命令行工具，运行：
```bash
$ python getWords.py
```

之后耐心等待爬取就好啦！爬取的数据会存放在`.\data\`目录下。
