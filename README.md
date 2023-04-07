# simplified-stock-exchange

Two main components:
- StockService
- DataStoreService

## StockService
-  StockService gets Trades and Dividends data from DataStoreService to compute:
    - dividend yield
    - PE ratio
    - volume weighted stock price
    - GBCE All Share Index
  
-  StockService can also post incoming Trades data to persist in DataStore.

## DataStoreService
-  DataStoreService stores accept and store incoming data including:
   - Most recent 5 mins trades data in a heap cache.
   - GBCE Dividend Data.
   
## How it works
The services are developed with Test Driven Development (TDD) approach. Therefore, it is easiest to understand how the service works by looking at the test cases at: https://github.com/darenwong/simplified-stock-exchange/blob/main/test/stockServiceTest.py
