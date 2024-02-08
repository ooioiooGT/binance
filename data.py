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

def getdata(symbol, timeframe, start_date):
    klines = client.get_historical_klines(symbol, timeframe, start_date)
    
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
    
    x = data_frame['Close']
    y = data_frame['Open']
    plt.plot(x)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage

while True:
    answer = input('''1. Hourly report
2. 15 mins report
3. 1 min report
4. Exit
Select an option (enter the corresponding number): ''')

    if answer in ['1', '2', '3']:
        symbol, start_date = user_input()
        
        if answer == '1':
            timeframe = client.KLINE_INTERVAL_1HOUR
            data_frame = getdata(symbol, timeframe, start_date)
            print('Hourly report:')
            print(data_frame)
            plot_chart(data_frame, 'Hourly Report')
            
        elif answer == '2':
            timeframe = client.KLINE_INTERVAL_15MINUTE
            data_frame = getdata(symbol, timeframe, start_date)
            print('15 mins report:')
            print(data_frame)
            plot_chart(data_frame, '15 mins report')

        elif answer == '3':
            timeframe = client.KLINE_INTERVAL_1MINUTE
            data_frame = getdata(symbol, timeframe, start_date)
            print('1 min report:')
            print(data_frame)
            plot_chart(data_frame, '1 min report')

    elif answer == '4':
        print('Exiting the program.')
        break

    else:
        print('Invalid input. Please enter a valid option.')
