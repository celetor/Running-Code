import os, time, json, base64, hashlib
import random
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ReadTimeout, HTTPError, RequestException

size_max = 6


def base64EncodeFile(byte, encode="utf-8"):
    # return "data:image/jpeg;base64," + str(base64.b64encode(byte), encode)
    return str(base64.b64encode(byte), encode)


def md5EncodeFile(byte):
    return hashlib.md5(byte).hexdigest()


def request(url, headers=None, data=None, method="GET"):
    try:
        if method == "GET":
            res = requests.get(url, headers=headers, timeout=10)
        else:
            res = requests.post(url, data=data, headers=headers, timeout=10)
        return res
    except ReadTimeout:
        print('timeout')
    except HTTPError:
        print('httperror')
    except RequestException:
        print('reqerror')


def wechat(data):
    url = os.environ.get('WECHAT_URL')
    headers = {
        'Content-Type': 'application/json',
    }
    return request(url, headers=headers, data=data, method="POST").text


def get_pic_url():
    index = random.randint(0,3)
    url = ['http://api.btstu.cn/sjbz/api.php?method={}&lx={}&format={}'.format('mobile', 'dongman', 'json'),
           'https://api.66mz8.com/api/rand.acg.php?type=二次元&format=json',
           'https://api.ixiaowai.cn/api/api.php?return=json',
           'https://api.apiopen.top/getImages?count=1']
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41"
    }
    print('get_pic_url',url[index])
    ret = request(url[index], headers=headers).text
    if index == 0:
        return json.loads(ret).get('imgurl')
    elif index == 1:
        return json.loads(ret).get('pic_url')
    elif index == 2:
        return json.loads(ret).get('imgurl')
    else:
        return json.loads(ret)['result'][0]['img']


def news_163():
    url = 'http://47.105.79.245/v2/article/newest'
    headers = {
        "User-Agent": "okhttp/3.10.0",
        "Content-Type": "application/json; charset=UTF-8"
    }
    data = '{"articleId":0,"feedId":98}'
    ret = request(url, headers=headers, data=data, method="POST").text
    news_list = json.loads(ret)['data']['data']
    article_list = []
    for i in range(size_max):
        article_list.append({
            "title": news_list[i]['title'],
            "description": news_list[i]['createTimeString'],
            "url": json.loads(request("http://47.105.79.245/v2/text/" + str(news_list[i]['id'])).text)['data'][
                'url'],
            "picurl": news_list[i]['thumbnail']
        })
    return article_list


def sougou_search(key):
    url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='.format(key)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41",
        'referer': 'https://weixin.sogou.com/'
    }
    ret = request(url, headers=headers).text
    soup = BeautifulSoup(ret, 'lxml').select_one('#sogou_vr_11002301_box_0')
    info = soup.select_one('dl:nth-child(3) > dd > a')
    pic = soup.select_one('img').attrs.get('src')
    other = soup.select_one('.tit em').text
    return [{
        "title": info.text,
        "description": other,
        "url": 'https://weixin.sogou.com/' + info.attrs.get('href'),
        "picurl": pic if str(pic).startswith('http') else 'https:' + pic
    }]


def jintiankansha():
    url = 'http://www.jintiankansha.me/column/qOcZgyKfdi'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41"
    }
    ret = request(url, headers=headers).text
    soups = BeautifulSoup(ret, 'lxml').select('.cell.item')
    article_list = []
    size = 0
    for soup in soups:
        if size < size_max:
            size = size + 1
            article_list.append({
                "title": soup.select_one('.item_title').text,
                "description": soup.select_one('.fade').text,
                "url": soup.select_one('.item_title>a').attrs.get('href'),
                "picurl": soup.select_one('.topic_image>img').attrs.get('src')
            })
        else:
            break
    return article_list


def qidian_booklist():
    url = 'https://www.qidiantu.com/booklists/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41"
    }
    ret = request(url, headers=headers).text
    soups = BeautifulSoup(ret, 'lxml').select('.panel-default')
    article_list = []
    size = 0
    for soup in soups:
        if size < size_max:
            size = size + 1
            time.sleep(2)
            article_list.append({
                "title": soup.select_one('h4').text,
                "description": soup.select_one('.panel-body').text,
                "url": 'https://www.qidiantu.com' + soup.select_one('.panel-heading>a').attrs.get('href'),
                "picurl": get_pic_url()
            })
        else:
            break
    return article_list

def youshu_booklist():
    url = 'https://www.yousuu.com/booklists/?type=man&screen=latest&page=1'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41"
    }
    ret = request(url, headers=headers).text
    soups = BeautifulSoup(ret, 'lxml').select('div.booklist-card')
    article_list = []
    size = 0
    for soup in soups:
        if size < size_max:
            size = size + 1
            time.sleep(3)
            pic = get_pic_url()
            print(size,pic)
            article_list.append({
                "title": soup.select_one('.booklist-card-content>a').text,
                "description": soup.select_one('.ResultBooklistItemClasses').text,
                "url": 'http://www.yousuu.com' + soup.select_one('.booklist-card-content>a').attrs.get('href'),
                "picurl": pic
            })
        else:
            break
    return article_list


def picture_json():
    url = get_pic_url()
    res = request(url)
    base64_code = base64EncodeFile(res.content)
    md5_code = md5EncodeFile(res.content)
    return {
        "base64": base64_code,
        "md5": md5_code
    }


def markdown_content():
    url = 'https://raw.githubusercontent.com/gedoor/legado/master/README.md'
    return request(url).text


def text_content():
    index = random.randint(0,2)
    url = ['https://v1.hitokoto.cn/?encode=json','https://api.ixiaowai.cn/ylapi/index.php/?code=json','https://api.66mz8.com/api/quotation.php?format=json']
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    print('text_content',url[index])
    ret = request(url[index], headers=headers).text
    if index == 0:
        return json.loads(ret).get('hitokoto')
    elif index == 1:
        return json.loads(ret).get('msg')
    else:
        return json.loads(ret).get('quotation')


if __name__ == '__main__':
    json_data = ''
    if os.environ.get('IS_TEXT') == 'TRUE':
        article = text_content()
        print(article)
        json_data = json.dumps({
            "msgtype": "text",
            "text": {
                "content": article
        }
    })
    # 图片类型
    elif os.environ.get('IS_PICTURE') == 'TRUE':
        article = picture_json()
        print(article)
        json_data = json.dumps({
            "msgtype": "image",
            "image": article
        })
    # markdown类型
    elif os.environ.get('IS_MARKDOWN') == 'TRUE':
        article = markdown_content()
        print(article)
        json_data = json.dumps({
            "msgtype": "markdown",
            "markdown": {
                "content": article
            }
        })
    # 图文类型
    else:
        articles = []
        if os.environ.get('IS_NEWS') == 'TRUE':
            articles = news_163()
        elif os.environ.get('IS_SOUGOU') == 'TRUE':
            articles = sougou_search('赤戟的书荒救济所')
        elif os.environ.get('IS_QIDIAN') == 'TRUE':
            articles = qidian_booklist()
        elif os.environ.get('IS_YOUSHU') == 'TRUE':
            articles = youshu_booklist()
        else:
            pass
        print(articles)

        json_data = json.dumps({
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        })

    ret = wechat(json_data)
    if json.loads(ret)['errcode'] == 0:
        print('发送成功')
    else:
        print('发送失败')
        print(ret)
