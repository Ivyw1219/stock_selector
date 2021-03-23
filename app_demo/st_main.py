import pandas as pd; import os
import streamlit as st
import time,datetime
import plotly.express as px;import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from main import Send_email

st.title('Demo of Smart Stock Selector')

st.sidebar.header('Build Your Stock Selector')

def file_selector(folder_path ='https://github.com/Ivyw1219/stock_selector/tree/main/app_demo/stock_data'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox("Select a Dataset",filenames)
    return os.path.join(folder_path, selected_filename)
    
filename = file_selector()
# st.info("You just selected {}".format(filename))

df = pd.read_csv(filename,sep= ',')
df = df.drop('Unnamed: 0', axis = 1)
###
    # show dataset
###if st.sidebar.checkbox("Show Dataset"):
##       number = st.number_input("Number of Rows to View:",5,10)
##        st.dataframe(df.head(number))
##
    # show columns
if st.sidebar.checkbox("Sort Stocks by Key Index"):
        all_cols = df.columns.to_list()
        selected_cols = st.sidebar.selectbox('Select a key index:', all_cols)
        st.dataframe(df.sort_values(by = selected_cols,ascending = False))
        # create a sidebar for a plot controls

if st.sidebar.subheader("How many stocks do you want to look?"):
    number = st.sidebar.number_input("Give a number:",10,100)

EPS_ranges = st.sidebar.slider('EPS Range', -10, 30,1) #(min,max,default)
Net_Profit_ranges = st.sidebar.slider('Net Proftis Range/million CNY', -50, 1000,10) #(min,max,default)
ROE_ranges = st.sidebar.slider('ROE Range', -5, 10,1)

#st.dataframe(df.sort_values(by = selected_cols,ascending = False))[0:ranges]

st.header('Overview')
eps_0_y = df[df['eps']<= 0].shape[0]
eps_1_y = df[(df['eps']>0) &(df['eps']<= 1)].shape[0]
eps_2_y = df[df['eps']>2].shape[0]
fig =px.pie(values= [eps_0_y,eps_1_y,eps_2_y],names = ['EPS<=0','EPS >0 & EPS <=1', 'EPS>2'],template = "plotly_white",title = 'EPS Distribution')
st.plotly_chart(fig)


st.write('1. There are {} stocks in the market.'.format(df.shape[0]))
st.write('2. {} percent of companies have negative EPS, only {} percent of companies EPS is greater than 2'.format(round(eps_0_y * 100/df.shape[0],2),round(eps_2_y* 100/df.shape[0],2)))
st.write('3. According to your selection, only {} stock EPS no less than {} and net profits no less than{} Million CNY.'
.format(df[df.eps > EPS_ranges].shape[0], EPS_ranges,Net_Profit_ranges))
st.write ('The percentage is {}%'.format(round(100* df[df.eps > EPS_ranges].shape[0]/df.shape[0],2)))

new_df = df[(df['eps']>= EPS_ranges) & (df['net_profits']>= Net_Profit_ranges )| 
(df['roe']>= ROE_ranges)].sort_values(by ='eps',ascending = False)[0:number]

np_0_y = df[df['eps']<= 0].shape[0]
np_1_y = df[(df['eps']>0) &(df['eps']<= 10000000)].shape[0]
np_2_y = df[df['eps']>10000000].shape[0]
fig =px.pie(values= [np_0_y,np_1_y,np_2_y],names = ['Net Profits<=0','Net Profits >0 & EPS <=10 Millon', 'EPS>10 Million'],template = "plotly_white",title = 'Net Profits Distribution')
st.plotly_chart(fig)

fig =px.box(df,y= 'eps', template = "plotly_dark",title = 'EPS Distribution')
st.plotly_chart(fig)


st.subheader('Sorting by EPS')
new_df = df[(df['eps']>= EPS_ranges) & (df['net_profits']>= Net_Profit_ranges )& 
(df['roe']>= ROE_ranges)].sort_values(by ='eps',ascending = False)[0:number]
fig =px.bar(new_df,x= 'eps', y = 'name',orientation='h',template = "plotly_dark")
st.plotly_chart(fig)

st.sidebar.header('Selected Stock Info')
st.sidebar.table(new_df[['code','name']])


st.subheader('Sorting by Net Profits')
fig =px.bar(new_df,x= 'net_profits', y = 'name',orientation='h',template = "plotly_dark")
fig.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=False)
st.plotly_chart(fig)

# automail part
Email_address = st.sidebar.text_input("Your Email Address:")
st.sidebar.info("Thank you! The result will send to your address soon")
df_sending = new_df[['code','name']].to_csv('https://github.com/Ivyw1219/stock_selector/tree/main/app_demo/stock_data/股票筛选结果.csv')
file_name_list = ['股票筛选结果.csv']
email_text = "%s股票筛选结果"%datetime.datetime.now().strftime('%Y%m%d %H')
recei_list = [Email_address]
Send_email(file_name_list,email_text,recei_list)
