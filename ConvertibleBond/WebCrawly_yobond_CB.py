import requests
import bs4


# 以下網址的表格一有更新便需要通知：
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


data = fetch(url)
root = bs4.BeautifulSoup(data, 'html.parser')
table = root.find('div', class_='content').find('table')

#找出表格內第一row的公司名稱，該公司名稱代表最新的資訊
def get_yobond_CB_data():
    newestName = table.find_all('tr')[2].find('a').text
    return newestName


#通知是否有表格有新資訊
def yobondCB_notify(oldDatastr_yobondcb):
    updated_yobond_dic = {}
    try:
        newDatastr_yobondcb=get_yobond_CB_data()
        if oldDatastr_yobondcb == newDatastr_yobondcb:
            #print(newDatastr_yoboundcb)
            print('yobond沒有更新表格')
        else:
            #print(newDatastr_yoboundcb)
            updated_yobond_dic=updatedDataDic(oldDatastr_yobondcb)

        return newDatastr_yobondcb, updated_yobond_dic
    except:
        print('悠債網，畫面有誤')
        newDatastr_yobondcb=oldDatastr_yobondcb
        return newDatastr_yobondcb, updated_yobond_dic


flag=0
def updatedDataDic(oldDatastr_yobondcb):
    updated_yobond_dic = {}

    global flag
    if (flag == 0):
        # updated_yobond_dic[companyName] = listingDate
        print('初始化紀錄yobond最新表格')
        flag = 1;
        return updated_yobond_dic

    index = 2
    while (True):
        companyName = table.find_all('tr')[index].find('a').text
        listingDate = table.find_all('tr')[index].find_all('td')[4].text.lstrip() #用lstrip()來清除開頭空白

        if (companyName == oldDatastr_yobondcb):
            break;
        else:
            updated_yobond_dic[companyName] = listingDate

        index = index + 1

    print('yobond更新!!!!!!!!!!!!!!!')
    return updated_yobond_dic



#
# asd = table.find_all('tr')[1]
# print(asd)
#
# newestName = table.find_all('tr')[2].find('a').text
# print(newestName)
#
# #用lstrip()來清除開頭空白
# listingDate = table.find_all('tr')[2].find_all('td')[4].text.lstrip()
# print(listingDate)


######################################TEST
# newestName=get_yobond_CB_data()
# print(newestName)

# newDatastr_yobondcb, updated_yobond_dic=yobondCB_notify({})
# print(newDatastr_yobondcb)
# print(updated_yobond_dic)
#
#
# newDatastr_yobondcb, updated_yobond_dic=yobondCB_notify(newDatastr_yobondcb)
# print(newDatastr_yobondcb)
# print(updated_yobond_dic)
#
# newDatastr_yobondcb, updated_yobond_dic=yobondCB_notify("聖暉一")
# print(newDatastr_yobondcb)
# print(updated_yobond_dic)