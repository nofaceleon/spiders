import datetime
import smtplib
from email.mime.text import MIMEText

def send_email(title, data):
    mail_host = "smtp.163.com"
    mail_user = 'xxxxx@163.com'
    mail_pass = 'xxxxxx'
    sender = 'xxxxx@163.com'
    receivers = ['xxxxx@qq.com']

    # 设置email信息
    # 邮件内容设置
    message = MIMEText(data, 'html', 'utf-8')
    # 邮件主题
    message['Subject'] = f"{datetime.date.today()}-{title}"
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(
            sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
        return 'success'
    except smtplib.SMTPException as e:
        return e
