from bs4 import BeautifulSoup
import requests
import time
import random
from product import product
import  mongoClient

startUrl="https://s.2.taobao.com/list/list.htm"  ##省略了部分

urlList=["https://s.2.taobao.com/list/list.htm?page={}&ist=1".format(str(i) )for i in range(1,10)]





def getParticular(url):

    data = requests.get("http:"+url, headers=headers2).text   ## header2 http 请求头
    return data[10:-3]


def getFlow(url):
    data=requests.get("http:"+url+"&callback=jsonp57" , headers=headers2).text
    return data.split(":")[1][0:-3]


def getProductInfo(url,headers2):
    data=requests.get(url,headers=headers2).text
    soup=BeautifulSoup(data,"lxml")
    productTitle  =soup.select("#J_Property > h1")
    productSeller =soup.select("#J_SellerInfo > div.simple > div.wangwang > a")
    price= soup.select("#J_Property > ul.price-info > li:nth-of-type(1) > span.price.big > em")
    costPrice=soup.select("#J_Property > ul.price-info > li:nth-of-type(2) > span:nth-of-type(2)")
    productCondition=soup.select("#J_Property > ul.idle-info > li:nth-of-type(1) > em")
    adders=soup.select("#J_Property > ul.idle-info > li:nth-of-type(2) > em")
    particulars=soup.select("#J_DescContent")
    flow=soup.select("#J_Browse")
    date=soup.select("#idle-detail > div.top-nav.clearfix > div.others-wrap > ul > li:nth-of-type(2) > span")

    title = productTitle if len(productTitle) == 0 else productTitle[0].get_text()
    seller = productSeller[0].get_text()
    price = price[0].get_text()
    cost = costPrice if len(costPrice) == 0 else costPrice[0].get_text()
    condition = productCondition[0].get_text()
    adder = adders[0].get_text()
    particular = getParticular(particulars[0].get("data-url"))
    flow = getFlow(flow[0].get("data-url"))
    date = date[0].get_text()

    return product(title,seller,price,cost,condition,adder,particular,flow,date)





getProductInfo("https://2.taobao.com/item.htm?id=537603922974&spm=2007.1000337.16.4.vbykfS",headers)


for indexUrl in urlList:
    data = requests.get(indexUrl, headers=headers).text
    soup=BeautifulSoup(data,"lxml")
    productUrl  =soup.select("#J_ItemListsContainer > div > div > div.item-info > div.item-pic > a")
    for url in productUrl:

        time.sleep(random.randint(15, 30))
        headers2["path"]=url.get("href")[14:-1]
        try:
            pro=getProductInfo("https:"+url.get("href")+"&spm=2007.1000337.16.4.vbykfS",headers)
            mongoClient.collection.insert(
                pro.__dict__
            )
        except  Exception as e:
            print('Error:', e)

