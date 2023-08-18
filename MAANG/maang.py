import streamlit as st
import yfinance as yf
import datetime

# Use the entire screen.
st.set_page_config(layout="wide")

# Insert containers as side-by-side columns.
col1, col2 = st.columns(2)

col1.write('''
# MAANG Stock Price App
''')

image_loc = "MAANG/maang_logo.png"
col2.image(image_loc)

col1.write("Stock Price and Volume Trends")
col1.write("Select a stock ticker and date range to see its historical trends.")

# Create three columns for the Data Selection widgets
col3, col4, col5 = st.columns(3)

# Create a dictionary to map full names to ticker symbols
ticker_mapping = {
    'Meta': 'META',
    'Apple': 'AAPL',
    'Amazon': 'AMZN',
    'Netflix': 'NFLX',
    'Google': 'GOOG'
}

# Create a dropdown selector for the stocks
ticker_name = col3.selectbox('Select ticker', list(ticker_mapping.keys()))

# Get the corresponding ticker symbol using the dictionary
tickerSymbol = ticker_mapping[ticker_name]

# Get the data on selected ticker
tickerData = yf.Ticker(tickerSymbol)

# Date Slider
start_date = col4.date_input('Starting Date', datetime.date(2010,1,1))
end_date = col5.date_input('Ending Date', datetime.date(2023,7,31))

# Get the historical prices for the selected ticker
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

col1, col2, col3, col4,col5,col6,col7 = st.columns(7)
col1.metric(":violet[Total Employees]", tickerData.info['fullTimeEmployees'],
            help = "Full Time Employees working in the Organization.")
col2.metric(":violet[Beta]", round(tickerData.info['beta'],3),
            help = "It indicates whether a stock is likely to be more volatile or less volatile than the market as a whole.")
col3.metric(":violet[Market Cap]", str(round(tickerData.info["marketCap"]/1000000000,1)) + "Bn",
            help = "How much is the entire company worth according to the stock market?")

profit_days = 0
loss_days = 0

for i in range(len(tickerDf)-1):
    if tickerDf.iloc[i+1,3] > tickerDf.iloc[i,3]:
        profit_days +=1
    else:
        loss_days += 1

col4.metric(":green[Highest Price]", round(tickerDf['Close'].max(),2),
            help = "Highest Price of the Stock in the selected period")
col5.metric(":red[Lowest Price]", round(tickerDf['Close'].min(),2),
            help = "Lowest Price of the Stock in the selected period")
col6.metric(":green[Days in  Profit]", profit_days,
            help = 'Number of days the stock closed in profit in the selected period.')
col7.metric(":red[Days in Loss]", loss_days,
            help = "Number of days the stock closed in loss  in the selected period.")

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 30px;
    font_family:monospace
}
</style>
""",
    unsafe_allow_html=True,
)
col1, col2 = st.columns(2)
# Create a button to toggle between Price and Volumen Trend charts
show_price_chart = col1.button('Show Price Trends Chart for Custom Dates')
show_volume_chart = col2.button('Show Volume Trends Chart for Custom Dates')

# Display the appropriate chart based on the button clicked

if show_price_chart:
    st.write(f'''Stock Price Trends for **{tickerData.info['longName']}** Company''')
    st.line_chart(tickerDf.Close, height=300)

if show_volume_chart:
    st.write(f'''Stock Traded Volume for **{tickerData.info['longName']}** Company''')
    st.line_chart(tickerDf.Volume, height=300)


# Create buttons for selecting time intervals
col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([2.5,1,1,1,1,1,1,1,1])
col1.markdown('***View Price and Volume Trends for the following Time Periods***')
day_1 = col2.button('1D')
day_5 = col3.button('5D')
month_1 = col4.button('1M')
month_6 = col5.button('6M')
ytd = col6.button('YTD')
year_1 = col7.button('1Y')
year_5 = col8.button('5Y')
year_max = col9.button('MAX')



tickerData = yf.Ticker(tickerSymbol)


if day_1:
    tickerDf = tickerData.history(period= '1d', interval = '1m')
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - 1 Day Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - 1 Day Interval')
    st.line_chart(tickerDf.Volume, height=300)

elif day_5:
    tickerDf = tickerData.history(period='5d', interval =  '30m')
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - 5 Days Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - 5 Days Interval')
    st.line_chart(tickerDf.Volume, height=300)
elif month_1:
    tickerDf = tickerData.history(period='1mo', )
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - 1 Month Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - 1 Month Interval')
    st.line_chart(tickerDf.Volume, height=300)
elif month_6:
    tickerDf = tickerData.history(period='6mo', )
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - 6 Months Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - 6 Months Interval')
    st.line_chart(tickerDf.Volume, height=300)
elif ytd:
    tickerDf = tickerData.history(period='ytd', )
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - Year To Date Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - Year To Date Interval')
    st.line_chart(tickerDf.Volume, height=300)
elif year_1:
    tickerDf = tickerData.history(period='1y', )
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - 1 Year Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - 1 Year Interval')
    st.line_chart(tickerDf.Volume, height=300)
elif year_5:
    tickerDf = tickerData.history(period='5y', )
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - 5 year Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - 5 year Interval')
    st.line_chart(tickerDf.Volume, height=300)
elif year_max:
    tickerDf = tickerData.history(period='max', )
    st.write(f'Stock Price Trends for **{tickerData.info["longName"]}** Company - Max Interval')
    st.line_chart(tickerDf.Close, height=300)
    st.write(f'Stock Traded Volume Trends for **{tickerData.info["longName"]}** Company - Max Interval')
    st.line_chart(tickerDf.Volume, height=300)

st.write('___')
st.write('Made by Rama Reddy Tadi')

