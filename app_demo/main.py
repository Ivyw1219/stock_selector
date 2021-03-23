# -*- coding: utf-8 -*-
''' automail  main.py '''
import smtplib 
import email
from  email.mime import multipart# import MIMEMultipart  
from  email.mime import text# import MIMEText  
from  email.mime import base# import MIMEBase  
import os.path
import mimetypes

#邮箱认证
def Send_email(file_name_list,email_text,recei_list):
    mail_info = {
        "from": "info@codewithivy.com",#自己的邮箱账号
        "to": "191022172@qq.com",#接收邮件的对方账号
        "hostname": "smtp.codewithivy.com",
        "username": "info@codewithivy.com",#开通smtp服务的邮箱账号
        "password": "#Babyseal2020#",#开通smtp服务的对应密码
        "mail_subject": "test",
        "mail_text": "hello, this is a test email, sended by python",
        "mail_encoding": "utf-8"
    }
    
    server = smtplib.SMTP_SSL(mail_info["hostname"],port=465)
    server.ehlo(mail_info["hostname"])
    server.login(mail_info["username"],mail_info["password"])#仅smtp服务器需要验证时

    # 构造MIMEMultipart对象做为根容器
    main_msg = multipart.MIMEMultipart()
    # 构造MIMEText对象做为邮件显示内容并附加到根容器  
    text_msg = text.MIMEText(email_text,_charset="utf-8")  
    main_msg.attach(text_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    for file_name in file_name_list:
        ## 读入文件内容并格式化 [方式1]
        data = open(file_name, 'rb')
        ctype,encoding = mimetypes.guess_type(file_name)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype,subtype = ctype.split('/',1)
        file_msg = base.MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        email.encoders.encode_base64(file_msg)#把附件编码

        ## 设置附件头
        basename = os.path.basename(file_name)
        file_msg.add_header('Content-Disposition','attachment', filename = basename,encoding='utf-8')
        main_msg.attach(file_msg)
    # 设置根容器属性
    main_msg['From'] = mail_info['from']  
    main_msg['To'] = ';'.join(recei_list)
    main_msg['Subject'] = email_text
    main_msg['Date'] = email.utils.formatdate()  

    #得到格式化后的完整文本
    fullText = main_msg.as_string() 

    #用smtp发送邮件
    try:
        server.sendmail(mail_info['from'], recei_list, fullText)  
    finally:
        server.quit()

