from binance.client import Client
import config
import pandas as pd 
import matplotlib.pyplot as plt

client = Client(config.apiKey, config.apiSecret, tld='us')

def user_input():
    symbol = input('What do you want to search: ').upper()
    hours_ago = int(input('Number of hours you want to see: '))
    start_date = f"{hours_ago} hour ago UTC"
    return symbol, start_date

def getdata():
    klines = client.get_historical_klines('ETHUSDT', client.KLINE_INTERVAL_1MINUTE, '1 hour ago UTC')
    
    # Extract relevant data and create a DataFrame
    df = pd.DataFrame(klines, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore'])
    
    # Keep only the columns you need
    df = df[['Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
    
    # Convert time to datetime format
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')
    
    # Set the 'Time' column as the DataFrame index
    df.set_index('Time', inplace=True)
    
    # Convert columns to numeric values
    df = df.apply(pd.to_numeric)
    
    return df
def plot_chart(data_frame, title):
    plt.figure(figsize=(10, 6))
    plt.subplot()
    x = data_frame.index
    y = data_frame['Close']

    plt.plot(y, label='Close Price', color='blue')

    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    plt.show()

data_frame = getdata()
def shortdata(data_frame):
    x = data_frame[['Open', 'Close']]
    file_path = 'open_close_data.csv'
    x.to_csv(file_path)
    return x


print (shortdata(data_frame))
# print(plot_chart(data_frame,'report'))