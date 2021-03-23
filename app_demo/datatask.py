from pandas import DataFrame
from main import Send_email
import datetime
import os
os.chdir('./')

df1 = DataFrame({'type':['a','b','c','d'],'value':[1,2,3,4]})
df2 = DataFrame({'type':['e','f','g','h'],'value':[5,6,7,8]})
df1.to_csv('df1.csv')
df2.to_csv('df2.csv')

#将2张表邮件发送
file_name_list = ['df1.csv','df2.csv']
email_text = "%s数据分析结果"%datetime.datetime.now().strftime('%Y%m%d %H')
recei_list = ['191022172@qq.com','ivy.w@veccoinsight.com']#写上自己的邮箱测试一下
Send_email(file_name_list,email_text,recei_list)