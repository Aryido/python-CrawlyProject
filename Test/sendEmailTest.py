import email.message
import smtplib

msg=email.message.EmailMessage()
msg["From"]="xxx"
msg["To"]="xxx"
msg["Subject"]="hi"

#寄送
msg.set_content("test")

#連線到SMTP SERVER
#gmail smtp server的資訊可上網查詢:
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("henryBitxxx", "nbrmoatftckitqam")
server.send_message(msg)
server.close()
