import requests
import bs4
from datetime import datetime

# 網址若有「公司債」關鍵字出現即通知：
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


# data = fetch(url)
# root = bs4.BeautifulSoup(data, 'html.parser')
# table = root.find('table')


# 取得最新有公司債的欄位，並回傳dic={時間:公司名}
def get_twse_CB_data():
    DataDic = {}

    data = fetch(url)
    root = bs4.BeautifulSoup(data, 'html.parser')
    table = root.find('table')

    # 找出最新所有新聞的內容
    newest_List = table.find('div', id='zoom01').find_all('form')[1].find('table').find_all('tr')[1:]  # 去掉最上面thead_row

    for theNews in newest_List:
        companyName = theNews.find_all('td')[1].text
        releaseDate = theNews.find_all('td')[2].text
        releaseTime = theNews.find_all('td')[3].text
        content = theNews.find_all('td')[4].text

        # 民國年換西元年
        AD_year = str(1911 + int(releaseDate[:3]))
        timeStr = AD_year + releaseDate[3:] + " " + releaseTime
        datetimeStrp = datetime.strptime(timeStr, "%Y/%m/%d %H:%M:%S")

        if ('公司債' in content):
            DataDic[str(datetimeStrp)] = companyName

    return DataDic



# 通知是否有新公司債資訊
flag = 0
def twseCB_notify(oldDataDic_twsecb):
    updateDataDic_twsecb = {}
    try:
        newDataDic_twsecb = get_twse_CB_data()
        global flag

        if newDataDic_twsecb:
            for key in newDataDic_twsecb.keys():
                if key in oldDataDic_twsecb.keys():
                    continue
                else:
                    updateDataDic_twsecb = updatedDataDic(oldDataDic_twsecb, newDataDic_twsecb)
                    return newDataDic_twsecb, updateDataDic_twsecb

            print("沒有新「公司債」相關新聞資訊")
            return newDataDic_twsecb, updateDataDic_twsecb
        else:
            print("目前無「公司債」相關新聞資訊")
            flag = 1
            return newDataDic_twsecb, updateDataDic_twsecb
    except:
        print("公開資訊網，全體公司類別畫面有誤")
        newDataDic_twsecb=oldDataDic_twsecb
        return newDataDic_twsecb, updateDataDic_twsecb


def updatedDataDic(oldDataDic_twsecb, newDataDic_twsecb):
    DataDic = {}

    global flag
    if flag == 0:
        flag = 1
        print('初始化「公司債」相關新聞資訊')
        return DataDic

    for newKey in newDataDic_twsecb:
        if newKey in oldDataDic_twsecb.keys():
            continue
        else:
            DataDic[newKey]=newDataDic_twsecb[newKey]

    print('有新「公司債」相關新聞資訊!!!!!!!!!!!!!!!')
    return DataDic

    # try:
    #     newest_List = table.find('div', id='zoom01').find_all('form')[1].find('table').find_all('tr')[1:]  # 去掉最上面row
    #
    #
    #     for theNews in newest_List:
    #         companyName = theNews.find_all('td')[1].text
    #         releaseDate = theNews.find_all('td')[2].text
    #         releaseTime = theNews.find_all('td')[3].text
    #         content = theNews.find_all('td')[4].text
    #
    #         # 民國年換西元年
    #         AD_year = str(1911 + int(releaseDate[:3]))
    #         timeStr = AD_year + releaseDate[3:] + " " + releaseTime
    #         datetimeStrp = datetime.strptime(timeStr, "%Y/%m/%d %H:%M:%S")
    #
    #         if (str(datetimeStrp) in oldDataDic_twsecb.keys()):
    #             continue
    #         else:
    #             if ('公司債' in content):
    #                 DataDic[str(datetimeStrp)] = companyName
    #
    #     print('有新「公司債」相關新聞資訊!!!!!!!!!!!!!!!')
    #     return DataDic
    # except:
    #     print("畫面有誤，等待下一次更新，或者直接重啟")
    #     return DataDic

######################################TEST
# dic=get_twse_CB_data()
# print(dic)
#
# newDataDic_twsecb, updateDataDic_twsecb=twseCB_notify({})
# print(newDataDic_twsecb)
# print(updateDataDic_twsecb)
