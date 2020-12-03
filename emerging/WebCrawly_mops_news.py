import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import bs4
from datetime import datetime

# 以下網址，在「市場別：興櫃公司」中，若有關鍵字「上櫃」相關新聞出現便需要通知：
driver = webdriver.Chrome()
driver.get("https://mops.twse.com.tw/mops/web/t05sr01_1")
time.sleep(2)
# selenium點選興櫃公司
selectedItemName = driver.find_element_by_xpath("//*[@id='table01']/form[1]/table/tbody/tr[2]/td[4]/input")
selectedItemName.click()


def getDriver_mopsNews():
    return driver

# 取得最新有「上櫃」相關新聞的欄位，並回傳dic={時間:公司名}
def get_mops_news_data():
    DataDic = {}

    try:
        # selenium點選興櫃公司
        selectedItemName = driver.find_element_by_xpath("//*[@id='table01']/form[1]/table/tbody/tr[2]/td[4]/input")
        selectedItemName.click()
        time.sleep(2)
        driver.find_element_by_name(name='fm_t05sr01_1')  # 如果沒抓到該表格就報錯，跳出
    except:
        raise



    try:
        # 迴圈超出範圍就報錯，跳出
        for i in range(2, 20, 1):
            companyName = driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[2]".format(i)).text
            releaseDate = driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[3]".format(i)).text
            releaseTime = driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[4]".format(i)).text
            content = driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[5]".format(i)).text
            # print(content)

            # 民國年換西元年
            AD_year = str(1911 + int(releaseDate[:3]))
            timeStr = AD_year + releaseDate[3:] + " " + releaseTime
            datetimeStrip = datetime.strptime(timeStr, "%Y/%m/%d %H:%M:%S")

            if ('上櫃' in content):
                DataDic[str(datetimeStrip)] = companyName
        return DataDic
    except:
        return DataDic



# 通知是否有新上櫃新聞資訊
flag = 0
def mopsNews_notify(oldDataDic_mopsNews_dic):
    updateDataDic_mopsNews = {}
    try:
        newDataDic_mopsNews_dic = get_mops_news_data()
        global flag

        if newDataDic_mopsNews_dic:
            for key in newDataDic_mopsNews_dic.keys():
                if key in oldDataDic_mopsNews_dic.keys():
                    continue
                else:
                    updateDataDic_mopsNews = updatedDataDic(oldDataDic_mopsNews_dic, newDataDic_mopsNews_dic)
                    return newDataDic_mopsNews_dic, updateDataDic_mopsNews

            print("沒有新「上櫃」相關新聞資訊")
            return newDataDic_mopsNews_dic, updateDataDic_mopsNews
        else:
            print("目前無「上櫃」相關新聞資訊")
            flag = 1
            return newDataDic_mopsNews_dic, updateDataDic_mopsNews
    except:
        print('print("公開資訊網，興櫃公司類別畫面有誤")')
        newDataDic_mopsNews_dic = oldDataDic_mopsNews_dic
        return newDataDic_mopsNews_dic, updateDataDic_mopsNews


def updatedDataDic(oldDataDic_mopsNews_dic, newDataDic_mopsNews_dic):
    updateDics = {}

    global flag
    if flag == 0:
        print('初始化「上櫃」相關新聞資訊')
        flag = 1
        return updateDics

    for newKey in newDataDic_mopsNews_dic:
        if newKey in oldDataDic_mopsNews_dic.keys():
            continue
        else:
            updateDics[newKey] = newDataDic_mopsNews_dic[newKey]

    print('「上櫃」相關新聞資訊更新!!!!!!!!!!!!!!!')
    return updateDics

    # try:
    #     for i in range(2, 20, 1):
    #         companyName = driver.find_element_by_xpath(
    #             "//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[2]".format(i)).text
    #         releaseDate = driver.find_element_by_xpath(
    #             "//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[3]".format(i)).text
    #         releaseTime = driver.find_element_by_xpath(
    #             "//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[4]".format(i)).text
    #         content = driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[5]".format(i)).text
    #
    #         # 民國年換西元年
    #         AD_year = str(1911 + int(releaseDate[:3]))
    #         timeStr = AD_year + releaseDate[3:] + " " + releaseTime
    #         datetimeStrp = datetime.strptime(timeStr, "%Y/%m/%d %H:%M:%S")
    #
    #         for key in oldDataDic_mopsNews_dic.keys():
    #             if (str(datetimeStrp) == key):
    #                 break
    #             else:
    #                 if ('上櫃' in content):
    #                     updateDics[str(datetimeStrp)] = companyName
    #
    #     print('「上櫃」相關新聞資訊更新!!!!!!!!!!!!!!!')
    #     return updateDics
    # except:
    #     return updateDics



# a=driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[2]".format(2)).text
# print(a)
#
# b=driver.find_element_by_xpath("//*[@id='table01']/form[2]/table/tbody/tr[{}]/td[2]".format(3)).text
# print(b)

# def erfun():
#     try:
#         a=1/0
#         print(1)
#     except:
#         print("error")
#         raise
# 
#     print('asdfasdfasd')
# 
# try:
#     erfun()
#     print(1)
# except:
#     print('yes!')