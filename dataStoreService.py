from collections import defaultdict
import heapq
from model.tradeData import TradeData

class DataStoreService:
  """
  DataStoreService stores accept and store incoming data including:
   - Most recent 5 mins trades data in a heap cache.
   - GBCE Dividend Data.
  """

  def __init__(self):
    self.tradesCache = defaultdict(list)
    self.dividendCache = self.getGBCEDividendData()

  def recordTrade(self, stock, timestamp, quantity, isBuy, price):
    currentTimestamp = self.getCurrentTimestamp()

    self.refreshTradesCache(currentTimestamp, stock)
    heapq.heappush(self.tradesCache[stock], [timestamp, TradeData(stock, timestamp, quantity, isBuy, price)])

  def refreshTradesCache(self, currentTimestamp, stock):
    if (len(self.tradesCache[stock]) == 0):
      return

    oldestAllowableTimestamp = currentTimestamp - 5*60
    while self.tradesCache[stock][0][0] < oldestAllowableTimestamp:
      heapq.heappop(self.tradesCache[stock])

  def getTrades(self, stock):
    currentTimestamp = self.getCurrentTimestamp()

    self.refreshTradesCache(currentTimestamp, stock)
    return self.tradesCache[stock]

  def getCurrentTimestamp(self):
    # In production, this should be returned from a time/clock server instead of using OS processing clock which can be inaccurate
    return 1680840759

  def getGBCEDividendData(self):
    # In production, this should be retrieved from the Global Beverage Corporation Exchange Server
    return {
      "TEA":{"Type":"Common","Last_Dividend":0,"Par_Value":100},
      "POP":{"Type":"Common","Last_Dividend":8,"Par_Value":100},
      "ALE":{"Type":"Common","Last_Dividend":23,"Par_Value":60},
      "JOE":{"Type":"Common","Last_Dividend":13,"Par_Value":250},
      "GIN":{"Type":"Preferred","Last_Dividend":8,"Fixed_Dividend":2,"Par_Value":100}
    }

