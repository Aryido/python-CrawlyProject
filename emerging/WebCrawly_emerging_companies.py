import requests
import bs4

# 抓取https://www.tpex.org.tw/，掛牌進度，最近登錄興櫃公司資料，若有更新即通知，
url = 'https://www.tpex.org.tw/web/regular_emerging/apply_schedule/applicant_emerging/applicant_emerging_companies.php?l=zh-tw'


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
table = root.find('table', class_='page-table')


def get_emerg_comp_data():
    ##找出表格內第一個公司名稱
    newestCompanyName = table.find('tbody').find('tr').find_all('td')[2].find('a').text
    return newestCompanyName

#通知是否有更新表格資訊
def emerg_comp_notify(oldDatastr_emerg_comp):
    updated_emerg_comp_dic = {}
    try:
        newDatastr_appli_comp = get_emerg_comp_data()
        if oldDatastr_emerg_comp == newDatastr_appli_comp:
            #print(newDatastr_appli_comp)
            print('登錄興櫃公司沒有更新表格')
        else:
            #print(newDatastr_appli_comp)
            updated_emerg_comp_dic=updatedDataDic(oldDatastr_emerg_comp)

        return newDatastr_appli_comp, updated_emerg_comp_dic
    except:
        print('tpex最近登錄興櫃公司，畫面有誤')
        newDatastr_appli_comp=""
        return newDatastr_appli_comp, updated_emerg_comp_dic

flag=0
def updatedDataDic(oldDatastr_emerg_comp):
   updated_appli_comp_dic={}
   global flag
   if (flag == 0):
       print("初始化紀錄最新登錄興櫃")
       flag = 1
       return updated_appli_comp_dic

   index = 0
   while(True):
       companyName = table.find('tbody').find_all('tr')[index].find_all('td')[2].find('a').text
       loginDate = table.find('tbody').find_all('tr')[index].find_all('td')[3].text

       if(companyName==oldDatastr_emerg_comp):
           break;
       else:
           updated_appli_comp_dic[companyName]= loginDate

       index = index + 1

   print('登錄興櫃公司更新表格!!!!!!!!!!!!!!!')
   return updated_appli_comp_dic




# a = table.find_all('tr')[0].find_all('td')[2].find('a').text
# print(a)
#
# b = table.find_all('tr')[1].find_all('td')[2].find('a').text
# print(b)
#
# c = table.find_all('tr')[1].find_all('td')[3].text
# print(c)

