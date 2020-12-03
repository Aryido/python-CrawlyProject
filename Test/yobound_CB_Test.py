import requests
import bs4
from lxml import etree

# 抓取https://www.tpex.org.tw/，申請上櫃公司資料
url = 'http://www.yobond.com.tw/Form/pub/'


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


##找出表格內第一個公司名稱，並儲存在再db或記事本裡，每15min，value若不相等則表示更新
data = fetch(url)
root=bs4.BeautifulSoup(data, 'html.parser')
table=root.find('div', class_='content').find('table')
#print(table)
#newestTrList=table.find_all('tr')[2:12]
#newestTr=table.find_all('tr')[2].find('a')


newestName=table.find_all('tr')[2].find('a').text
print(newestName)




