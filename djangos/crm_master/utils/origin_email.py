# https://www.cnblogs.com/saneri/p/5845048.html
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

import os

# 登陆邮件服务器
smtpObj = smtplib.SMTP('smtp.qq.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
# 传入相应的账号密码信息
smtpObj.login('973697101@qq.com', 'tungwiacnhxubcgg')

# 邮件收发信人信息
sender = '973697101@qq.com'  # 发件人信息
receivers = ['363396239@qq.com']  # 收件人信息

# 完善发件人收件人，主题信息
message = MIMEMultipart()
message['From'] = formataddr(["发件人昵称", sender])
message['To'] = formataddr(["收件人昵称", ''.join(receivers)])
subject = 'Python SMTP 邮件， 包括html和附件整体混合邮件'
message['Subject'] = Header(subject, 'utf-8')

# 正文部分
textmessage = MIMEText('<p>Python SMTP2 ,html文本</p>' +
                       '<p>主要参考： <a href="https://www.cnblogs.com/saneri/p/5845048.html">Python SMTP邮件模块</a></p>' +
                       '<p><img src="G:\test_Python\AutomateTheBoringStuffWithPythonTest\16EmailAndMessageTest\picture001.jpg"/></p>',
                       'html', 'utf-8')
message.attach(textmessage)

# # 附件部分，此处尝试添加txt，图片，word，pdf，表格，音乐文4类
# workLoc = os.path.join('G:\\', 'test_Python', 'AutomateTheBoringStuffWithPythonTest', '16EmailAndMessageTest')
# print('预设存放表格路径为:' + str(workLoc))
# # 检查路径有效性
# textFile = 'text001.txt'
# print("文本附件文件名为：%s" % textFile)
# textFileLoc = os.path.join(workLoc, textFile)
# textAtt = MIMEText(open(textFileLoc, 'rb').read(), 'base64', 'utf-8')
# textAtt["Content-Type"] = 'application/octet-stream'
# # 这里的filename可以任意写，但是实际测试如果在线查看及下载查看，名称默认为此处设置的名字，所以后续直接就是原始附件名，方便下载、在线查看
# textAtt.add_header('Content-Disposition', 'attachment', filename=textFile)
# message.attach(textAtt)
# # 尝试添加图片附件
# pictureFile = 'picture001.jpg'
# print("图片附件文件名为：%s" % pictureFile)
# pictureFileLoc = os.path.join(workLoc, pictureFile)
# pictureAtt = MIMEApplication(open(pictureFileLoc, 'rb').read())
# pictureAtt.add_header('Content-Disposition', 'attachment', filename=pictureFile)
# message.attach(pictureAtt)
# # 尝试添加word附件
# wordFile = 'word001.doc'
# print("word附件文件名为：%s" % wordFile)
# wordFileLoc = os.path.join(workLoc, wordFile)
# wordAtt = MIMEText(open(wordFileLoc, 'rb').read(), 'base64', 'utf-8')
# wordAtt.add_header('Content-Disposition', 'attachment', filename=wordFile)
# message.attach(wordAtt)
# # 尝试添加表格附件
# sheetFile = 'sheet001.xls'
# print("表格附件文件名为：%s" % sheetFile)
# sheetFileLoc = os.path.join(workLoc, sheetFile)
# sheetAtt = MIMEText(open(sheetFileLoc, 'rb').read(), 'base64', 'utf-8')
# sheetAtt.add_header('Content-Disposition', 'attachment', filename=sheetFile)
# message.attach(sheetAtt)
# # 尝试添加pdf附件
# pdfFile = 'pdf001.pdf'
# print("表格附件文件名为：%s" % pdfFile)
# pdfFileLoc = os.path.join(workLoc, pdfFile)
# pdfAtt = MIMEText(open(pdfFileLoc, 'rb').read(), 'base64', 'utf-8')
# pdfAtt.add_header('Content-Disposition', 'attachment', filename=pdfFile)
# message.attach(pdfAtt)
# # 尝试添加声音wav附件
# musicFile = 'music001.wav'
# print("表格附件文件名为：%s" % musicFile)
# musicFileLoc = os.path.join(workLoc, musicFile)
# musicAtt = MIMEApplication(open(musicFileLoc, 'rb').read())
# musicAtt.add_header('Content-Disposition', 'attachment', filename=musicFile)
# message.attach(musicAtt)

# 发送邮件操作
smtpObj.sendmail(sender, receivers, message.as_string())
smtpObj.quit()
print("脚本运行结束")
