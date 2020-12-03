import requests
import bs4


#抓取https://www.tpex.org.tw/，申請上櫃公司資料
url = 'https://www.tpex.org.tw/web/regular_emerging/apply_schedule/applicant/applicant_companies.php?l=zh-tw'

def fetch(url):
    #附加request Header資訊
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    #獲取response
    response = requests.get(url, headers=headers)

    #若獲取成功，則回傳，若否則exception
    if response.status_code != 200:
        raise Exception(response.content)

    return response.content.decode('utf-8')



##找出表格內第一個公司名稱，並儲存在再db或記事本裡，每15min，value若不相等則表示更新
data=fetch(url)
print(data)
root=bs4.BeautifulSoup(data, 'html.parser')
#print(root.table.tbody)

index=root.find("tbody")
# print(index)
# print(type(index))
# print(len(index.select('td>a')))
print(index.select('td>a')[0].text)
# print(index.select('td>a')[2].text)
# for i in range(0,len(index.select('td>a')),2):
#     print(index.select('td>a')[i].text)








