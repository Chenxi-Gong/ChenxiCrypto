#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
A cryptocurrency analysis tool implemented by Chen'xi Gong.
Last updated at 2022/01/30.
'''

import requests
import time
import matplotlib.pyplot as plt

class FetchData:
    def __init__(self):
        self.url = 'https://api.kucoin.com/api/v1/market/candles'
    
    def request(self, symbol, startAt, endAt, ttype):
        endAt = int(endAt) + 1
        params = {'symbol':symbol, 'startAt':startAt, 'endAt':endAt, 'type':ttype}
        while True:
            r = requests.get(self.url, params = params)
            text = r.text
            if 'Too Many Requests' in text:
                time.sleep(10)
                continue
            break
        if 'This pair is not provided at present' in text:
            print('wrong symbol name')
            return 'error'
        return text
    
    def tolist(self, text):
        self.startPoint = text.index('data') + 8
        text = text[self.startPoint:-1]
        to_list = text.split('[')
        newlist = []
        for i in range(len(to_list)):
            rowtext = to_list[len(to_list)-i-1][:-2]
            rowlist = rowtext.split(',')
            newrow = []
            for j in range(len(rowlist)):
                if j == 0:
                    newrow.append(int(rowlist[j][1:-1]))
                else:
                    newrow.append(float(rowlist[j][1:-1]))
            newlist.append(newrow)
        return newlist
    
    def ttostamp(self, t):
        timeArray = time.strptime(t, '%Y-%m-%d %H:%M:%S')
        timeStamp = str(int(time.mktime(timeArray)))
        return timeStamp
    
    def stamptot(self, timeStamp):
        timeArray = time.localtime(timeStamp)
        t = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return t
    
    def alltostamp(self, startAt, endAt):
        self.startAt = startAt
        self.endAt = endAt
        if len(self.startAt) > 10:
            self.startAt = self.ttostamp(self.startAt)
        if len(self.endAt) > 10:
            self.endAt = self.ttostamp(self.endAt)
        self.startAt = int(self.startAt)
        self.endAt = int(self.endAt)
        return self.startAt, self.endAt
    
    def timeStamp(self, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        symbol = 'BTC-USDT'
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[0])
        return newlist
    
    def time(self, startAt, endAt, ttype):
        timeStampList = self.timeStamp(startAt, endAt, ttype)
        if timeStampList == 'error':
            return 'error'
        newlist = []
        for i in timeStampList:
            newlist.append(self.stamptot(i))
        return newlist
    
    def opening(self, symbol, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[1])
        return newlist
    
    def close(self, symbol, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[2])
        return newlist
    
    def high(self, symbol, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[3])
        return newlist
    
    def low(self, symbol, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[4])
        return newlist
    
    def volume(self, symbol, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[5])
        return newlist
    
    def amount(self, symbol, startAt, endAt, ttype):
        startAt, endAt = self.alltostamp(startAt, endAt)
        text = self.request(symbol, startAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        newlist = []
        for i in datalist:
            newlist.append(i[6])
        return newlist
    
    def MA(self, symbol, startAt, endAt, ttype, infotype, k):
        infolist = ['open', 'close', 'high', 'low', 'volume', 'amount']
        index = infolist.index(infotype) + 1
        startAt, endAt = self.alltostamp(startAt, endAt)
        MAstartAt = startAt - 60 * (k - 1)
        text = self.request(symbol, MAstartAt, endAt, ttype)
        if text == 'error':
            return 'error'
        datalist = self.tolist(text)
        MAlist = []
        for i in range(len(datalist)):
            if i >= k - 1:
                sumvalue = 0
                for j in range(k):
                    sumvalue += datalist[i-j][index]
                MAlist.append(float(sumvalue/k))
        return MAlist

    def RS(self, symbol, inference_symbol, startAt, endAt, ttype, infotype):
        infolist = ['open', 'close', 'high', 'low', 'volume', 'amount']
        index = infolist.index(infotype) + 1
        startAt, endAt = self.alltostamp(startAt, endAt)
        objectText = self.request(symbol, startAt, endAt, ttype)
        if objectText == 'error':
            return 'error'
        inferenceText = self.request(inference_symbol, startAt, endAt, ttype)
        if inferenceText == 'error':
            return 'error'
        objectDatalist = self.tolist(objectText)
        inferenceDatalist = self.tolist(inferenceText)
        RSlist = []
        for i in range(len(objectDatalist)):
            RSlist.append(float(objectDatalist[i][index]/inferenceDatalist[i][index]))
        return RSlist
    
class Simulation:
    def __init__(self):
        self.data = FetchData()
        self.ttype = '1min'
        self.symbol = 'BTC-USDT'
        self.startAt = None
        self.endAt = None
        self.record = None
        self.profit = None
    
    def buySignal(self):
        buyPercent = 0
        return buyPercent

    def sellSignal(self):
        sellPercent = 0
        return sellPercent
    
    def simulate(self):
        self.cash = 10000.0
        self.initCash = self.cash
        self.stock = 0.0
        self.stockValue = 0.0
        self.timeList = self.data.timeStamp(self.startAt, self.endAt, self.ttype)
        self.priceList = self.data.close(self.symbol, self.startAt, self.endAt, self.ttype)
        self.record = []
        for i in range(len(self.timeList)):
            self.i = i
            buyPercent = self.buySignal()
            self.stock += self.cash * buyPercent / self.priceList[i]
            self.cash -= self.cash * buyPercent
            sellPercent = self.sellSignal()
            self.cash += self.stock * sellPercent * self.priceList[i]
            self.stock -= self.stock * sellPercent
            self.stockValue = self.stock * self.priceList[i]
            self.record.append([self.i, self.timeList[i], self.priceList[i], buyPercent, sellPercent, self.cash, self.stock, self.stockValue])
        self.profit = (self.cash + self.stock * self.priceList[-1] - self.initCash)/self.initCash
        self.simpleProfit = (self.priceList[-1] - self.priceList[1])/self.priceList[1]
    
    def visual(self):
        x = []
        y = []
        for i in self.record:
            x.append(i[0])
            y.append(i[2])
        plt.plot(x, y, linewidth = (len(self.record)+200)/2000, color = (0.5, 0.5, 0.5))
        for i in self.record:
            plt.scatter(i[0], i[2], s = (len(self.record)+1000)/2000, color = (i[7]/(i[5]+i[7]), i[5]/(i[5]+i[7]), 0))

