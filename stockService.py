

class StockService:
  """
  StockService gets Trades and Dividends data from DataStoreService to compute:
    - dividend yield
    - PE ratio
    - volume weighted stock price
    - GBCE All Share Index
  
  StockService can also post incoming Trades data to persist in DataStore.
  """

  def __init__(self, dataStoreService):
    self.dataStoreService = dataStoreService
  
  def getDividendYield(self, stock, price):
    dividendData = self.dataStoreService.dividendCache[stock]

    if dividendData["Type"] == "Common":
      return dividendData["Last_Dividend"]/price
    elif dividendData["Type"] == "Preferred":
      return dividendData["Fixed_Dividend"]*dividendData["Par_Value"]*0.01/price
    
    raise KeyError("Dividend data not found")

  def getPERatio(self, stock, price):
    return price/self.getDividendYield(stock, price)

  def getVolumeWeightedStockPrice(self, stock):
    trades = self.dataStoreService.getTrades(stock)
    sumTradedPriceQuantity = 0
    sumQuantity = 0

    for _, tradeData in trades:
      sumQuantity += tradeData.quantity
      sumTradedPriceQuantity += tradeData.price*tradeData.quantity
    return sumTradedPriceQuantity/sumQuantity

  def getGBCEAllShareIndex(self):
    cumulativeProductVolumeWeightedStockPrice = 1
    numStocks = 0

    for stock in self.dataStoreService.tradesCache:
      cumulativeProductVolumeWeightedStockPrice *= self.getVolumeWeightedStockPrice(stock)
      numStocks += 1
    
    return cumulativeProductVolumeWeightedStockPrice**(1.0/float(numStocks))

  def recordTrade(self, stock, timestamp, quantity, isBuy, price):
    self.dataStoreService.recordTrade(stock, timestamp, quantity, isBuy, price)