import time
from selenium import webdriver
from datetime import datetime

# 以下網址的表格一有更新便需要通知：
driver = webdriver.Chrome()
driver.get("https://www.tpex.org.tw/web/bond/publish/convertible_bond_search/memo.php?l=zh-tw")
time.sleep(2)  # 等待網頁script跑完，才會自動排序

def getDriver_tpse_CB():
    return driver

def get_tpse_CB_data():
    newDatastr_tpexcb = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[1]/td[2]").text
    return newDatastr_tpexcb


# 通知是否有更新表格資訊
def tpexCB_notify(oldDatastr_tpexcb):
    updated_tpex_dic = {}
    try:
        newDatastr_tpexcb = get_tpse_CB_data()
        if oldDatastr_tpexcb == newDatastr_tpexcb:
            # print(newDatastr_tpexcb)
            print('tpex債卷市場沒有更新表格')
        else:
            # print(newDatastr_tpexcb)
            updated_tpex_dic = updatedDataDic(oldDatastr_tpexcb)

        return newDatastr_tpexcb, updated_tpex_dic
    except:
        print('tpex債卷市場,畫面有誤')
        newDatastr_tpexcb = oldDatastr_tpexcb
        return newDatastr_tpexcb, updated_tpex_dic


flag = 0
def updatedDataDic(oldDatastr_tpexcb):
    updated_tpexcb_dic = {}
    global flag
    if (flag == 0):
        # updated_tpexcb_dic[Name] = (issuingDate + " ~ " + maturityDate)
        flag = 1
        print('初始化紀錄tpex債卷市場')
        return updated_tpexcb_dic

    index = 1
    while (True):
        Name = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[{}]/td[2]".format(index)).text
        issuingDate = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[{}]/td[4]".format(index)).text
        maturityDate = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[{}]/td[5]".format(index)).text

        if (Name == oldDatastr_tpexcb):
            break;
        else:
            nowTime_YMD = str(datetime.now()).split('.')[0].split(" ")[0]
            datetimeStrip_nowTime_YMD = datetime.strptime(nowTime_YMD, "%Y-%m-%d")
            datetimeStrip_issuingDate = datetime.strptime(issuingDate, "%Y/%m/%d")
            diff_days = (datetimeStrip_nowTime_YMD - datetimeStrip_issuingDate).days
            if (diff_days > 0):
                index = index + 1
                continue
            else:
                updated_tpexcb_dic[Name] = (issuingDate + " ~ " + maturityDate)
                index = index + 1

    print('tpex債卷市場更新!!!!!!!!!!!!!!!')
    return updated_tpexcb_dic

# newDatastr_tpexcb = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[1]/td[2]").text
# print(newDatastr_tpexcb)
#
# issuingDate = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[1]/td[4]").text
# print(issuingDate)
#
# maturityDate = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[1]/td[5]").text
# print(maturityDate)

# print(str(datetime.now()).split('.')[0].split(" ")[0])
# nowTime_YMD=str(datetime.now()).split('.')[0].split(" ")[0]
# datetimeStrip_nowTime_YMD = datetime.strptime(nowTime_YMD, "%Y-%m-%d")
# print(datetimeStrip_nowTime_YMD)
#
# issuingDate = driver.find_element_by_xpath("//*[@id='rpt_result']/tbody/tr[{}]/td[4]".format(1)).text
# print(issuingDate)
# datetimeStrip_issuingDate = datetime.strptime(issuingDate, "%Y/%m/%d")
# print(datetimeStrip_issuingDate)
#
# print((datetimeStrip_nowTime_YMD-datetimeStrip_issuingDate).days)
# # print((datetimeStrip_issuingDate-datetimeStrip_nowTime_YMD).days)
# diff_days=(datetimeStrip_nowTime_YMD-datetimeStrip_issuingDate).days
# print(type(diff_days))
