#以下網址，在「市場別：興櫃公司」中，若有關鍵字「上櫃」相關新聞出現便需要通知：
url = 'https://mops.twse.com.tw/mops/web/t05sr01_1'


def fetch(url):
    # 附加request Header資訊
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    # 獲取response
    response = requests.get(url, headers=headers)

    # 若獲取成功，則回傳，若否則exception
    if response.status_code != 200:
        raise Exception(response.content)

    return response.content.decode('utf-8')

data = fetch(url)
root=bs4.BeautifulSoup(data, 'html.parser')

#找出最新10則新聞的內容
table=root.find('table')
newest_10_List=table.find('div', id='zoom01').find_all('form')[1].find('table').find_all('tr')[1:11]

for theNews in newest_10_List:
    content=theNews.find_all('td')[4].text
    print(content)
    if('上櫃' in content):
        print("有新上櫃資訊")
    else:
        print('目前沒新的上櫃資訊')
    print("==============")