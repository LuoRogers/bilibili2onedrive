#根据自己的情况修改9，11，17行。

import smtplib
def sendmail(to,title,message):
    from email.mime.text import MIMEText
    from email.header import Header

    # 邮箱用户名
    sender = "发件邮箱"
    # 邮箱密码
    password = "邮箱密码，一般为授权码"#
    # 收件人 无论是否只有一个收件人 都必须是列表
    receiver = [to, ]
    # 邮件正文
    message = MIMEText(message, "plain", "utf-8")
    # 发件人显式的名字
    message["From"] = Header("收件人名字", "utf-8")
    # 收件人显式的名字
    message["To"] = Header(to, "utf-8")
    # 邮件标题
    message["Subject"] = title
    try:
        # 使用qq企业邮箱服务器发送
        smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登陆
        smtp.login(sender, password)
        # 发送
        smtp.sendmail(sender, receiver, message.as_string())
        print("邮件已发送")
    except smtplib.SMTPException as e:
        print("Error! 发送失败", e)
