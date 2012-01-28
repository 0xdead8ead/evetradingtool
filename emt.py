#!/usr/bin/env python
import os
#import urllib
import urllib2
from BeautifulSoup import BeautifulSoup


class EveDataProcessor:
    
    def getPageSource(self, eveCentralAPI):
        '''Retrieves XML from Eve Central API'''
        response = urllib2.urlopen(eveCentralAPI)
        pageSource = response.read()
        return pageSource
    
    def parseAverages(self, pageSource):
        '''Parses Eve Central XML Data for Average Volume Sold and Median of Sales'''
        soupBowl = BeautifulSoup(pageSource)
        volumeTag = str(soupBowl.evec_api.marketstat.type.sell.volume)
        volumeValue = volumeTag.replace('<volume>','').replace('</volume>','')
        
        medianTag = str(soupBowl.evec_api.marketstat.type.sell.median)
        medianValue = medianTag.replace('<median>','').replace('</median>','')
        
        volumeValue = float(volumeValue)
        medianValue = float(medianValue)
        
        return volumeValue, medianValue


    def parseProfit(self, pageSource):
        soupBowl = BeautifulSoup(pageSource)
        sellTag = str(soupBowl.evec_api.quicklook.sell_orders.order.price)
        sellValue = sellTag.replace('<price>','').replace('</price>','')

        buyTag = str(soupBowl.evec_api.quicklook.buy_orders.order.price)
        buyValue = buyTag.replace('<price>','').replace('</price>','')
        
        sellValue = float(sellValue)
        buyValue = float(buyValue)
        
        return sellValue, buyValue
    
    def retrieveData(self, itemID, systemID):
        xmlDataMarketStat = self.getPageSource("http://api.eve-central.com/api/marketstat?typeid="+str(itemID)+"&usesystem="+str(systemID))
        volumeQuantity, avgPrice = self.parseAverages(xmlDataMarketStat)
        
        xmlDataQuickLook = self.getPageSource("http://api.eve-central.com/api/quicklook?typeid="+str(itemID)+"&usesystem="+str(systemID))
        lowSell, highBuy = self.parseProfit(xmlDataQuickLook)
        return {"volumeQuantity": volumeQuantity, "avgPrice": avgPrice, "lowSell": lowSell, "highBuy": highBuy, "itemID": itemID, "systemID": systemID}
        
        
        


    pass

eve = EveDataProcessor();

'''
xmlDataMarketStat = eve.getPageSource("http://api.eve-central.com/api/marketstat?typeid=209&usesystem=30000142")
volumeQuantity, avgPrice = eve.parseAverages(xmlDataMarketStat)

xmlDataQuickLook = eve.getPageSource("http://api.eve-central.com/api/quicklook?typeid=209&usesystem=30000142")
lowSell, highBuy = eve.parseProfit(xmlDataQuickLook)
'''
#avgQuantity = float(raw_input('\nAverage Quantity Sold:'))

marketData = eve.retrieveData(191, 30000142)

volumeQuantity = marketData["volumeQuantity"]
avgPrice = marketData["avgPrice"]
lowSell = marketData["lowSell"]
highBuy = marketData["highBuy"]

avgQuantity = volumeQuantity



#avgPrice = float(raw_input('\nAverage Prince:'))
#lowSell = float(raw_input('\nLowest Sell Price:'))
#highBuy = float(raw_input('\nHighest Buy Price:'))

iskFlow = float(avgQuantity) * float(avgPrice)
profitSpread = ((float(lowSell) / float(highBuy)) - 1)*100
print "_________________________________________"
print "\n\nISK Flow Per Day: %.2f\n" % iskFlow
if (iskFlow > 1000000000):
    print "Over a billion isk flow?: YES!"
else:
    print "Over a billion isk flow?: no :("
    
print "Profit Spread: %d%%\n" % profitSpread

doInvest = raw_input("Would you like to invest?(Y,n)")
if (doInvest == "n"):
    os._exit(0)
else:
    investmentCapital = float(raw_input("How much would you like to invest?"))
    buyQuantity = investmentCapital / highBuy
    potentialReturn = buyQuantity * lowSell
    profit = potentialReturn - investmentCapital
    if (iskFlow > 1000000000):
        investmentScore = (iskFlow / 1000000000) * profitSpread
    else:
        investmentScore = 0
    
    print "Volume of Sales: %.2f\n" % volumeQuantity
    print "Investment of %.2f:\n" % investmentCapital
    print "Quantity to Buy: %.2f\n" % buyQuantity
    print "Potential Return: %.2f\n\n" % potentialReturn
    print "Potential Profit: %.2f\n\n" % profit
    print "Investment Score: %.2f\n" % investmentScore
    
    
    
    
    
    