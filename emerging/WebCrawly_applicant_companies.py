import requests
import bs4

# 抓取https://www.tpex.org.tw/，申請上櫃公司資料，網址的表格一有更新便需要通知：
url = 'https://www.tpex.org.tw/web/regular_emerging/apply_schedule/applicant/applicant_companies.php?l=zh-tw'


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
table = root.find('table')
tbody = root.find("tbody")
thead = root.find("thead")


def get_appli_comp_data():
    ##找出表格還沒有填完的部分
    RevisableFormDic = saveRevisableForm()

    return RevisableFormDic


# 通知是否有更新表格資訊
def appli_comp_notify(oldRevisableFormDic_appli_comp):
    newUpdated_appli_comp_dic = {}
    try:
        newRevisableFormDic_appli_comp = get_appli_comp_data()
        if (oldRevisableFormDic_appli_comp):
            for key in newRevisableFormDic_appli_comp.keys():
                if key not in oldRevisableFormDic_appli_comp.keys():
                    applyDate = newRevisableFormDic_appli_comp[key]["applyDate"]
                    newUpdated_appli_comp_dic[key] = "申請日期: "+str(applyDate)
                else:
                    for valueDic_key in newRevisableFormDic_appli_comp[key].keys():
                        if (newRevisableFormDic_appli_comp[key][valueDic_key] != oldRevisableFormDic_appli_comp[key][
                            valueDic_key]):
                            #applyDate = newRevisableFormDic_appli_comp[key]["applyDate"]
                            newUpdated_appli_comp_dic[key] = str(valueDic_key)+": "+str(newRevisableFormDic_appli_comp[key][valueDic_key])
                            break

            if(newUpdated_appli_comp_dic):
                print("申請上櫃公司更新表格!!!!!!!!!!!!!!!")
                return newRevisableFormDic_appli_comp, newUpdated_appli_comp_dic
            else:
                print("申請上櫃公司沒有更新表格")

        else:
            print("初始化申請上櫃公司表格")

        return newRevisableFormDic_appli_comp, newUpdated_appli_comp_dic
    except:
        print('tpex申請上櫃公司資料表，畫面有誤')
        newRevisableFormDic_appli_comp=oldRevisableFormDic_appli_comp
        return newRevisableFormDic_appli_comp, newUpdated_appli_comp_dic


def saveRevisableForm():
    trs = table.find_all('tr')

    RevisableFormDic = {}  # key:companyName，value:Json
    for i in range(1, len(trs), 1):
        reviewDate = trs[i].find_all('td')[6].text  # 上櫃審議委員會審議日期
        listingDate = trs[i].find_all('td')[7].text  # 櫃買董事會通過上櫃日期
        agreeListingDate = trs[i].find_all('td')[8].text  # 櫃買同意上櫃契約日期
        stockListingDate = trs[i].find_all('td')[9].text  # 股票上櫃買賣日期
        offeringPrice = trs[i].find_all('td')[11].text  # 承銷價
        remark = trs[i].find_all('td')[12].text  # 備註

        # 備註有"自撤"，代表不會再更新，故不用儲存該row資訊
        if ("自撤" in remark):
            continue

        tr_Head = trs[0].find_all('th')
        reviewDate_title = tr_Head[6].text
        listingDate_title = tr_Head[7].text
        agreeListingDate_title = tr_Head[8].text
        stockListingDate_title = tr_Head[9].text
        offeringPrice_title = tr_Head[11].text
        remark_title = tr_Head[12].text

        if(i==1):
            dic = {}
            dic["applyDate"] = trs[i].find_all('td')[3].text
            dic[reviewDate_title] = reviewDate
            dic[listingDate_title] = listingDate
            dic[agreeListingDate_title] = agreeListingDate
            dic[stockListingDate_title] = stockListingDate
            dic[offeringPrice_title] = offeringPrice
            dic[remark_title] = remark
            RevisableFormDic[trs[i].find_all('td')[2].text] = dic

        if (reviewDate == "") or (listingDate == "") or (agreeListingDate == "") or (stockListingDate == "") or (
                offeringPrice == ""):
            dic = {}
            dic["applyDate"] = trs[i].find_all('td')[3].text
            dic[reviewDate_title] = reviewDate
            dic[listingDate_title] = listingDate
            dic[agreeListingDate_title] = agreeListingDate
            dic[stockListingDate_title] = stockListingDate
            dic[offeringPrice_title] = offeringPrice
            dic[remark_title] = remark
            RevisableFormDic[trs[i].find_all('td')[2].text] = dic

    return RevisableFormDic


# newDatastr_appli_comp = get_appli_comp_data()
# print(newDatastr_appli_comp)
#
# updated_appli_comp_dic=updatedDataDic(newDatastr_appli_comp)
# print(updated_appli_comp_dic)
#
# a=tbody.select('td>a')[0].text
# print(a)
#
# b=tbody.select('td>a')[1].text
# print(b)
#
# c=tbody.select('td>a')[2].text
# print(c)
#
# d=tbody.select('td>a')[3].text
# print(d)
#
#
# newestCompanyName = tbody.find('tr').find_all('td')[2].find('a').text
# print(newestCompanyName)
# print("==================")
# tds = tbody.find_all('tr')[1].find_all('td')
#
# for td in tds:
#     print(td.text)
# print("==================")
#
# a=tds[9]
# print(a.text)
# print(type(a.text))
#
# if(a.text==""):
#     print(1)
# else:
#     print(0)
#
# print("==================")

# trs = tbody.find_all('tr')
# #print(trs)
# for tr in trs:
#     a = tr.find_all('td')[6].text
#     b = tr.find_all('td')[7].text
#     c = tr.find_all('td')[8].text
#     d = tr.find_all('td')[9].text
#     e = tr.find_all('td')[11].text
#     f = tr.find_all('td')[12].text
#     # print("{},{},{},{},{},{}".format(a,b,c,d,e,f))
#     if ("自撤" in f):
#         continue
#
#     if (a == "") or (b == "") or (c == "") or (d == "") or (e == ""):
#         print(tr.find_all('td')[2].text)
#         print(tr.find_all('td')[3].text)
#         print("==================")


# trs_Head=thead.find_all('tr')
#
# for tr in table.find_all('tr'):
#     print(tr.text)


# trs = table.find_all('tr')
# # print(trs)
# tr_head = trs[0]
# print(tr_head.find_all('th'))


#RevisableFormDic = saveRevisableForm()
# print(RevisableFormDic)

# dic=RevisableFormDic['臺慶科']
# print(dic)
# jObj=json.loads(dic)

# print(jObj)


# dic={}
#
# dic1={"1":"one"}
#
# for key in dic1.keys():
#     if key not in dic.keys():
#         print("key not in dic.keys()")
#     else:
#         print("key  in dic.keys()")

# a=root.find("123")
# print(a)