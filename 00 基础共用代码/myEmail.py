# 设置qq邮箱完毕
import smtplib
from email.header import Header
from email.mime.text import MIMEText

sender = '2909755020@qq.com'  # 发送使用的邮箱
receivers = ['2909755020@qq.com']  # 收件人，可以是多个任意邮箱

message = MIMEText('这里是正文！', 'plain', 'utf-8')
message['From'] = Header("发送者", 'utf-8')  # 发送者
message['To'] = Header("接收者", 'utf-8')  # 接收者

subject = '这里是主题！'
message['Subject'] = Header(subject, 'utf-8')

try:
    # qq邮箱服务器主机
    # 常见其他邮箱对应服务器：
    # qq:smtp.qq.com 登陆密码：系统分配授权码
    # 163:stmp.163.com 登陆密码：个人设置授权码
    # 126:smtp.126.com 登陆密码：个人设置授权码
    # gmail:smtp.gmail.com 登陆密码：邮箱登录密码

    smtp = smtplib.SMTP_SSL('smtp.qq.com')

    # 登陆qq邮箱，密码需要使用的是授权码
    smtp.login(sender, 'wudyfyafvxfwddaf')

    smtp.sendmail(sender, receivers, message.as_string())
    smtp.quit()
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")