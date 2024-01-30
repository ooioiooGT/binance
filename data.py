from binance.client import Client
import config

client = Client(config.apiKey,config.apiSecret , tld='us')
info = client.get_symbol_info('BNBBTC')
for i in info:
    print(i)
