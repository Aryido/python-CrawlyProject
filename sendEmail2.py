import email.message
import smtplib

# 建立全域變數-興櫃相關網址
appli_comp_url = "https://www.tpex.org.tw/web/regular_emerging/apply_schedule/applicant/applicant_companies.php?l=zh-tw"
mops_news_url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
emerg_comp_url = "https://www.tpex.org.tw/web/regular_emerging/apply_schedule/applicant_emerging/applicant_emerging_companies.php?l=zh-tw"


# 建立全域變數-可轉債相關網址
yobond_CB_url="http://www.yobond.com.tw/Form/pub/"
tpex_CB_url="https://www.tpex.org.tw/web/bond/publish/convertible_bond_search/memo.php?l=zh-tw"
twse_CB_url="https://mops.twse.com.tw/mops/web/t05sr01_1"

def sendEmailMsg(appli_comp_dic, updateDataDic_mopsNews, updated_emerg_comp_dic, updated_yobond_dic, updated_tpex_dic, updateDataDic_twsecb):
    msg = email.message.EmailMessage()
    msg["From"] = "weitingliu421@gmail.com"
    msg["To"] = "f104882013@gmail.com"


    msg["Subject"] = "興櫃、可轉債相關更新內容"

    ############################以下興櫃相關
    strHtml = "<h1><a href='{}'>申請上櫃，新增以下公司</a></h1>".format(appli_comp_url)
    for key in appli_comp_dic.keys():
        strHtml = strHtml + "<h4>{} {}</h4>".format(key, appli_comp_dic[key])

    strHtml = strHtml + "<p>==========</p><br><h1><a href='{}'>興櫃公司的上櫃相關新聞，新增以下公司</a></h1>".format(mops_news_url)
    for key in updateDataDic_mopsNews.keys():
        strHtml = strHtml + "<h4>{} 發言時間: {}</h4>".format(updateDataDic_mopsNews[key], key)

    strHtml = strHtml + "<p>==========</p><br><h1><a href='{}'>最近登錄興櫃公司，新增以下公司</a></h1>".format(emerg_comp_url)
    for key in updated_emerg_comp_dic:
        strHtml = strHtml + "<h4>{} 登入日期: {}</h4>".format(key, updated_emerg_comp_dic[key])
    ############################以上興櫃相關

    ############################以下可轉債相關
    strHtml = strHtml + "<p>==========</p><br><h1><a href='{}'>悠債網，新增以下公司</a></h1>".format(yobond_CB_url)
    for key in updated_yobond_dic:
        strHtml = strHtml + "<h4>{} 掛牌日期: {}</h4>".format(key, updated_yobond_dic[key])

    strHtml = strHtml + "<p>==========</p><br><h1><a href='{}'>債券市場資訊，新增以下公司</a></h1>".format(tpex_CB_url)
    for key in updated_tpex_dic:
        strHtml = strHtml + "<h4>{} 發行日期: {}</h4>".format(key, updated_tpex_dic[key])

    strHtml = strHtml + "<p>==========</p><br><h1><a href='{}'>公司債相關新聞，新增以下公司</a></h1>".format(twse_CB_url)
    for key in updateDataDic_twsecb:
        strHtml = strHtml + "<h4>{} 發言時間: {}</h4>".format(updateDataDic_twsecb[key], key)
    ############################以上可轉債相關

    # 寄送
    msg.set_content("test")
    msg.add_alternative(strHtml, subtype="html")

    # 連線到SMTP SERVER
    # gmail smtp server的資訊可上網查詢
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # 申請gmail應用程式密碼教學網址: https://www.youtube.com/watch?v=YQboCnlOb6Y&t=853s
    server.login("weitingliu421@gmail.com", "isezbocxmrsttvle")
    server.send_message(msg)
    server.close()
