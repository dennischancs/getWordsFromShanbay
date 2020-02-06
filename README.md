# 修改
1. 改账号登陆为Cookies登陆;
2. 由于shanbay.com改变了单词书链接，但单词书的Lists链接没变，故依据[原项目2019-06提供的wordlist.json](https://github.com/likeke1997/getWordsFromShanbay)抓取了所有词表;
3. 爬取结果见`.\data\wordsSelected.json`。


# [原说明](https://github.com/likeke1997/getWordsFromShanbay)

这是我用 Python 写的爬虫，能爬取扇贝网里的单词书和单词列表。使用到的库有`request`、`bs4`、`json`。

爬取结果展示（节选自`.\data\wordsSelected.json`）：

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
categories = loadJSON('wordlist)

# 配置登录信息
userAccount = 'likeke'
userPassword = '123456'

# 配置需要爬取的单词书类别 category 和数量 count
selectBooks = [
    {'category': '四级', 'count': '5'},
    {'category': '六级', 'count': '3'},
    {'category': '考研', 'count': '2'}
]
```

然后打开命令行工具，运行：
```bash
$ python test.py
```

之后耐心等待爬取就好啦！爬取的数据会存放在`.\data\`目录下。目录下已存在的几个`.json`文件都是我爬取好的数据，可作为参考或直接使用。
