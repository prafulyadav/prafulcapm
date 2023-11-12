import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import pandas_datareader.data as web
import datetime
import capm_functions


st.set_page_config(page_title = "CAPM" , page_icon = " chart_with_upwards_trend" , layout='wide')
# st.set_page_config(page_title = "CAPM" , page_icon = " chart_with_upwards_trend" )

st.title("CAPITAL ASSEST PRINCING MODEL ")

# input from users

col1,col2= st.columns([1,1])
with col1:
 stocklist = st.multiselect("choose 4 stocks",('TSLA','AAPL','NFLX','GOOGL'),['TSLA','AAPL','NFLX','GOOGL'])
with col2:
 year=st.number_input("Number of Year",1,10)

# download data SP500

# try:
end =datetime.date.today()
start = datetime.date(datetime.date.today().year - year,datetime.date.today().month,datetime.date.today().day)
SP500=web.DataReader(['sp500'],'fred',start,end)
print(SP500.tail())

# new data frame
stocks_df=pd.DataFrame()

for stock in stocklist:
    data= yf.download(stock , period=f'{year}y')
    # print(data.head())
    stocks_df[f'{stock}']=data['Close']

# print(stocks_df.head())

# -------------exact date------------#
stocks_df.reset_index(inplace=True)
SP500.reset_index(inplace=True)
SP500.columns=['Date','sp500']
stocks_df['Date']=stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date']=stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date']=pd.to_datetime(stocks_df['Date'])
stocks_df=pd.merge(stocks_df,SP500,on='Date',how='inner')
# print(stocks_df)

col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Dataframe head")
    st.dataframe(stocks_df.head(),use_container_width=True)
with col2:
    st.markdown("### Dataframe  tail")
    st.dataframe(stocks_df.tail(),use_container_width=True)



# --------plotly

col1,col2=st.columns([1,1])
with col1:
    st.markdown("### price of all stock")
    st.plotly_chart(capm_functions.interactive_plot(stocks_df))
with col2:
#    capm_functions.normalize(stocks_df)   print it for check the data
    st.markdown("### price of all stock (After Normalize)")
    st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))   


 #---------daily
stocks_daily_return = capm_functions.dailyret(stocks_df) 
print(stocks_daily_return.head())

# --------beta and alpha value

beta={}
alpha={}

for i in stocks_daily_return.columns:
   if i!='Date'and i!='sp500':
      b,a=capm_functions.cal_beta(stocks_daily_return,i)

      beta[i]=b
      alpha[i]=a
print(beta,alpha)    

beta_df=pd.DataFrame(columns=['Stock','Beta Value'])
beta_df['Stock']=beta.keys()
beta_df['Beta Value']=[str(round(i,2)) for i in beta.values()]

with col1:
    st.markdown("### Calculated Beta Value")
    st.dataframe(beta_df,use_container_width=True)

rf=0
rm= stocks_daily_return['sp500'].mean()*252

return_df=pd.DataFrame()
return_value=[]
for stock ,value in beta.items():
   return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df['Stock']=stocklist
return_df['Return Value']=return_value 

with col2:
    st.markdown("### Calculated Return Value using CAPM")
    st.dataframe(return_df,use_container_width=True)



# except:
#     st.write("Select karo pehele Valid Input")
