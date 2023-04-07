import unittest
from unittest.mock import MagicMock
import sys
sys.path.append("..")

from dataStoreService import DataStoreService
from stockService import StockService
from collections import defaultdict

class StockServiceTest(unittest.TestCase):

  def setUp(self):
    self.dataStoreService = DataStoreService()
    self.dataStoreService.getGBCEDividendData = MagicMock(return_value=self.getSampleDividendData())

    self.stockService = StockService(self.dataStoreService)

  def tearDown(self):
    self.dataStoreService.tradesCache = defaultdict(list)

  def testGetDividendYield(self):
    self.assertEqual(self.stockService.getDividendYield("POP", 2), 4)
    self.assertEqual(self.stockService.getDividendYield("POP", 4), 2)
    self.assertEqual(self.stockService.getDividendYield("GIN", 2), 1)

  def testGetPERatio(self):
    self.assertEqual(self.stockService.getPERatio("POP", 2), 0.5)
    self.assertEqual(self.stockService.getPERatio("POP", 4), 2)
    self.assertEqual(self.stockService.getPERatio("GIN", 2), 2)

  def testGetVolumeWeightedStockPrice(self):
    self.dataStoreService.getCurrentTimestamp = MagicMock(return_value=1680840759)

    self.dataStoreService.recordTrade("POP", 1680840758, 1, True, 10)
    self.dataStoreService.recordTrade("POP", 1680840757, 2, True, 16)
    self.assertEqual(self.stockService.getVolumeWeightedStockPrice("POP"), 14)

    # Do not include data from more than 5 minutes ago in calculation
    self.dataStoreService.recordTrade("POP", 1580840757, 2, True, 16)
    self.assertEqual(self.stockService.getVolumeWeightedStockPrice("POP"), 14)

  def testGetGBCEAllShareIndex(self):
    self.dataStoreService.getCurrentTimestamp = MagicMock(return_value=1680840759)

    self.dataStoreService.recordTrade("POP", 1680840758, 1, True, 10)
    self.dataStoreService.recordTrade("POP", 1680840757, 2, True, 16)
    self.dataStoreService.recordTrade("TEA", 1680840757, 1, True, 10)
    self.dataStoreService.recordTrade("TEA", 1680840756, 2, True, 16)

    self.assertEqual(self.stockService.getGBCEAllShareIndex(), 14)

  def getSampleDividendData(self):
    return {
      "TEA":{"Type":"Common","Last_Dividend":0,"Par_Value":100},
      "POP":{"Type":"Common","Last_Dividend":8,"Par_Value":100},
      "ALE":{"Type":"Common","Last_Dividend":23,"Par_Value":60},
      "JOE":{"Type":"Common","Last_Dividend":13,"Par_Value":250},
      "GIN":{"Type":"Preferred","Last_Dividend":8,"Fixed_Dividend":2,"Par_Value":100}
    }

if __name__ == '__main__':
    unittest.main()