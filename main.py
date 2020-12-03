from emerging import WebCrawly_applicant_companies as applicomp
from emerging import WebCrawly_mops_news as mopsnews
from emerging import WebCrawly_emerging_companies as emergcomp
import sendEmail
import sendEmail2

from ConvertibleBond import WebCrawly_twse_CB as twsecb
from ConvertibleBond import WebCrawly_yobond_CB as yobondcb
from ConvertibleBond import WebCrawly_tpex_CB as tpexcb

import schedule
import time
from datetime import datetime

# 建立全域變數-興櫃相關
oldRevisableFormDic_appli_comp = {}
oldDataDic_mopsNews = {}
oldDatastr_emerg_comp = ""
def emergingJob():
    global oldRevisableFormDic_appli_comp, oldDataDic_mopsNews, oldDatastr_emerg_comp

    newRevisableFormDic_appli_comp, newUpdated_appli_comp_dic = applicomp.appli_comp_notify(
        oldRevisableFormDic_appli_comp)
    newDataDic_mopsNews, updateDataDic_mopsNews = mopsnews.mopsNews_notify(oldDataDic_mopsNews)
    newDatastr_emerg_comp, updated_emerg_comp_dic = emergcomp.emerg_comp_notify(oldDatastr_emerg_comp)

    # 更新全域變數-興櫃相關
    oldRevisableFormDic_appli_comp = newRevisableFormDic_appli_comp
    oldDataDic_mopsNews = newDataDic_mopsNews
    oldDatastr_emerg_comp = newDatastr_emerg_comp

    return newUpdated_appli_comp_dic, updateDataDic_mopsNews, updated_emerg_comp_dic


# 建立全域變數-可轉債相關
oldDatastr_yoboundcb = ""
oldDatastr_tpexcb = ""
oldDataDic_twsecb = {}
def convertibleBondJob():
    global oldDatastr_yoboundcb, oldDatastr_tpexcb, oldDataDic_twsecb

    newDatastr_yoboundcb, updated_yobond_dic = yobondcb.yobondCB_notify(oldDatastr_yoboundcb)
    newDatastr_tpexcb, updated_tpex_dic = tpexcb.tpexCB_notify(oldDatastr_tpexcb)
    newDataDic_twsecb, updateDataDic_twsecb = twsecb.twseCB_notify(oldDataDic_twsecb)

    # 更新全域變數-可轉債相關
    oldDatastr_yoboundcb = newDatastr_yoboundcb
    oldDatastr_tpexcb = newDatastr_tpexcb
    oldDataDic_twsecb = newDataDic_twsecb

    return updated_yobond_dic, updated_tpex_dic, updateDataDic_twsecb


def job():
    global oldRevisableFormDic_appli_comp, oldDataDic_mopsNews, oldDatastr_emerg_comp, \
        oldDatastr_yoboundcb, oldDatastr_tpexcb, oldDataDic_twsecb
    print("I'm working...")
    print(str(datetime.now()).split('.')[0])

    # 興櫃相關回傳的更新資料
    newUpdated_appli_comp_dic, updateDataDic_mopsNews, updated_emerg_comp_dic = emergingJob()
    print(newUpdated_appli_comp_dic)
    print(updateDataDic_mopsNews)
    print(updated_emerg_comp_dic)
    print(oldRevisableFormDic_appli_comp.keys())
    print(oldDataDic_mopsNews)
    print(oldDatastr_emerg_comp)

    # 可轉債相關回傳的更新資料
    updated_yobond_dic, updated_tpex_dic, updateDataDic_twsecb = convertibleBondJob()
    print(updated_yobond_dic)
    print(updated_tpex_dic)
    print(updateDataDic_twsecb)
    print(oldDatastr_yoboundcb)
    print(oldDatastr_tpexcb)
    print(oldDataDic_twsecb)


    try:
        # 重新刷新tpex頁面
        driver__mopsNews = mopsnews.getDriver_mopsNews()
        driver__mopsNews.refresh()
        time.sleep(2)
        # selenium點選興櫃公司
        selectedItemName = driver__mopsNews.find_element_by_xpath("//*[@id='table01']/form[1]/table/tbody/tr[2]/td[4]/input")
        selectedItemName.click()

        # 重新刷新tpex頁面
        driver_tpexcb = tpexcb.getDriver_tpse_CB()
        time.sleep(1)
        driver_tpexcb.refresh()
    except:
        print('畫面刷新，請等下次更新')
        driver__mopsNews.refresh()
        driver_tpexcb.refresh()


    # 寄信判斷，並傳入更新的資料
    if (newUpdated_appli_comp_dic or updateDataDic_mopsNews or updated_emerg_comp_dic or \
            updated_yobond_dic or updated_tpex_dic or updateDataDic_twsecb):
        sendEmail.sendEmailMsg(newUpdated_appli_comp_dic, updateDataDic_mopsNews, updated_emerg_comp_dic,
                                updated_yobond_dic, updated_tpex_dic, updateDataDic_twsecb)
        # sendEmail2.sendEmailMsg(newUpdated_appli_comp_dic, updateDataDic_mopsNews, updated_emerg_comp_dic,
        #                         updated_yobond_dic, updated_tpex_dic, updateDataDic_twsecb)
        print("已寄信")

    print("END====================================")



# 設定排程時間
#schedule.every(20).seconds.do(job)
schedule.every(15).minutes.do(job)
print("Staring...")
print("     ")
while True:
    # 啟動schedule
    schedule.run_pending()


