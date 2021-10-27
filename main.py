from PySimpleGUI.PySimpleGUI import Input
import pandas as pd
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from http_request_randomizer.requests.proxy.requestProxy import RequestPr
# import chromedriver_binary
import csv
import time
import sys
import os
import requests
import json
import PySimpleGUI as sg
import urllib
# import itertools
import random
import threading
import tkinter
from tkinter import messagebox
import math
from twocaptcha import TwoCaptcha

from io import StringIO
from selenium.webdriver.chrome.options import Options
# from urllib import request, parse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requestium import Session, Keys
from ebaysdk import response
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from ebaysdk.policies import Connection as Policies
import re
import mysql.connector
class ScrapePlaces:

    #process product title
    def processTitle(self,product_title,omitwordList):
         new_title=''
         for omitword in omitwordList:
            if product_title.find(omitword)!=-1:
                product_title=product_title.replace(omitword,'')
         for k in product_title.split("\n"):
            letter = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
            print(letter)
            new_title=new_title + letter
         print(len(new_title))
         if len(new_title)>78:
             new_title = new_title[:75]+"..."
         return new_title    
    #save omit word
    def omitwordSave(self,omitwords):
        omitwordFile = open("omitwords.txt",'w',encoding="utf-8")
        omitwordFile.write(omitwords)
        omitwords = omitwordFile
        print(omitwords)
    #if title length is less than 50, add "from Japan"
    def addTitle(self,title):
        new_title = title
        if len(title)<50:
            new_title = title + " from Japan"
        return new_title    
    # add new product on ebay function
    def addNewProductOnEbay (self,omitwordList,title,price,imageurls,count,category,brand,product_state,categoryID,paymentpolicy,returnpolicy,shippingpolicy,paymentId,returnId,shippingId,requiredItems,requiredValues):

            new_title=scrap.processTitle(title,omitwordList)
            print(new_title)
            print(len(new_title))
            focal_length=""   
            aperture=""
            if category=="レンズ":
                try:
                   result = re.search("([0-9])\w+mm",title,re.M|re.I)
                   if result!=None:
                     print( result.group())
                     focal_length = result.group() 
                except:
                    focal_length=""
                    pass
                try: 
                    result1 = re.search("[Ff][0-9]*\.[0-9]+",title,re.M|re.I)
                    if result1==None:
                        result2 = re.search("[Ff]/[0-9]+",title,re.M|re.I)
                        if result2==None:
                            aperture = "None"
                        else:
                            aperture = result2.group()    
                    else:
                        aperture=result1.group()        
                except:
                    pass
                print(aperture)
                # new_title="Nikon AF MICROaaa NIKKOR 60mm F2.8 D"
                # focal_length="50mm"
                # aperture="F/2"
                focal_length_type="Manual,Fixed/prime"    
                descriptionFile = open("description.txt",'r',encoding="utf8")
                description=descriptionFile.readlines()
                print(description)
                product_brand = brand
                print(categoryID)
                print(paymentpolicy,returnpolicy,shippingpolicy)
                print(paymentId,returnId,shippingId)
                print(category)
              

                print("=============Image Uploading===========")
                try:    
                    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "Item":{
                                        "Title":"{}".format(new_title),
                                        "BestOfferDetails":{
                                            "BestOfferEnabled":"true"
                                        },
    
                                        "Description":"<![CDATA{0}]>".format(description),
                                        "ListingDuration":"GTC",
                                        "ListingType":"FixedPriceItem",
                                        "Location":"Japan",
                                        "StartPrice":"{}".format(price),
                                        "Country":"JP",
                                        "Currency":"USD",
                                        "Quantity":"{}".format(count),
                                        "ConditionID":"{}".format(product_state),
                                        "ProductListingDetails":{
                                            "ItemSpecifics":{
                                               "Brand":"CONTINENTAL",
                                               "IncludeeBayProductDetails":"true",
                                               "Mount":"Canon EF",
                                               "Type":"standard"
                                            }
                                                     
                                        },
                                        "ItemSpecifics":{
                                            "NameValueList":[
                                                {
                                                    "Name":"Brand",
                                                    "Value":"{}".format(product_brand)
                                                },
                                            {
                                                    "Name":"Type",
                                                    "Value":"Standard,Telephoto"
                                                },
                                            {
                                                    "Name":"Mount",
                                                    "Value":"{} F".format(product_brand)
                                                },
                                                {
                                                    "Name":"Focal Length",
                                                    "Value":"{}".format(focal_length)
                                                },
                                            {
                                                    "Name":"Maximum Aperture",
                                                    "Value":"{}".format(aperture)
                                                },
                                            {
                                                    "Name":"Focal Length Type",
                                                    "Value":"{}".format(focal_length_type)
                                                },
                                            
                                            {
                                                    "Name":"Country/Region of Manufacture",
                                                    "Value":"Japan"
                                                },
                                                
                                            {
                                                    "Name":"Compatible Brand",
                                                    "Value":"For {}".format(product_brand)
                                                }
                                            
                                            
                                            ]
                                        },
                                        "PaymentMethods":"PayPal",
                                        "PayPalEmailAddress":"kevinzoo.lancer@gmail.com",
                                        "DispatchTimeMax":"1",
                                        "ShipToLocations":"None",
                                        "ReturnPolicy":{
                                            "ReturnsAcceptedOption":"ReturnsAccepted",
                                            "ReturnsWithinOption":"Days_30"
                                        },
                                        "PrimaryCategory":{
                                            "CategoryID":"3323"
                                        },
                                        "PictureDetails":{
                                            "PictureURL":imageurls,
                                        },
                                        "ItemCompatibilityList":{
                                                "Compatibility":{
                                                    "NameValueList":[
                                                        {"Name":"Year","Value":"2010"},
                                                        {"Name":"Make","Value":"Hummer"},
                                                        {"Name":"Model","Value":"H3"}
                                                    ],
                                                    "CompatibilityNotes":"An example compatibility"
                                                }
                                        },

                                        "SellerProfiles":{

                                                "SellerPaymentProfile":{
                                                   
                                                        "PaymentProfileName":"{}".format(paymentpolicy[0]),  
                                                        "PaymentProfileID":"{}".format(paymentId)
                                                        },
                                                        "SellerReturnProfile":{
                                                  
                                                        "ReturnProfileName":"{}".format(returnpolicy[0]),  
                                                        "ReturnProfileID":"{}".format(returnId)
                                                        },
                                                        "SellerShippingProfile":{
                                                      
                                                        "ShippingProfileName": "{}".format(shippingpolicy[0]),
                                                        "ShippingProfileID":"{}".format(shippingId) 
                                                        },
                                        } ,
        
        
                                        
                                        "Site":"US"

                                }
                                        
                
                    }
                    response=api.execute("AddItem", request)
                    print(response.dict())
                    print(response.reply)
                except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass

            elif category=="フィルムカメラ" or category=="デジタルカメラ":
                 focal_length_type="Fixed/prime"    
                 cameradescriptionFile = open("cameradescription.txt",'r',encoding="utf8")
                 cameradescription=cameradescriptionFile.readlines()
                 product_brand = brand
                 print(categoryID)
                 print(paymentpolicy,returnpolicy,shippingpolicy)
                 print(paymentId,returnId,shippingId)
                 print(category)
                 try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "Item":{
                                        "Title":"{}".format(new_title),
                                         "BestOfferDetails":{
                                            "BestOfferEnabled":"true"
                                        },
                                        "Description":"<![CDATA{0}]>".format(cameradescription),
                                        "ListingDuration":"GTC",
                                        "ListingType":"FixedPriceItem",
                                        "Location":"Beverly Hills",
                                        "StartPrice":"{}".format(price),
                                        "Country":"JP",
                                        "Currency":"USD",
                                        "Quantity":"{}".format(count),
                                        "ConditionID":"{}".format(product_state),
                                        "ProductListingDetails":{
                                            "ItemSpecifics":{
                                               "Brand":"CONTINENTAL",
                                               "IncludeeBayProductDetails":"true",
                                               "Mount":"Canon EF",
                                               "Type":"standard"
                                            }
                                                     
                                        },
                                        "ItemSpecifics":{
                                            "NameValueList":[
                                                {
                                                    "Name":"Brand",
                                                    "Value":"{}".format(product_brand)
                                                },
                                            {
                                                    "Name":"Type",
                                                    "Value":"Standard"
                                                },
                                            {
                                                    "Name":"Model",
                                                    "Value":"{} FD".format(product_brand)
                                                }
                                               
                                            
                                            ]
                                        },
                                        "PaymentMethods":"PayPal",
                                        "PayPalEmailAddress":"kevinzoo.lancer@gmail.com",
                                        "DispatchTimeMax":"1",
                                        "ShipToLocations":"None",
                                        "ReturnPolicy":{
                                            "ReturnsAcceptedOption":"ReturnsNotAccepted"
                                        },
                                        "PrimaryCategory":{
                                            "CategoryID":"31388"
                                        },
                                        "PictureDetails":{
                                            "PictureURL":imageurls,
                                        },
                                        "ItemCompatibilityList":{
                                                "Compatibility":{
                                                    "NameValueList":[
                                                        {"Name":"Year","Value":"2010"},
                                                        {"Name":"Make","Value":"Hummer"},
                                                        {"Name":"Model","Value":"H3"}
                                                    ],
                                                    "CompatibilityNotes":"An example compatibility"
                                                }
                                        },
                                      
                                        "SellerProfiles":{

                                                "SellerPaymentProfile":{
                                                   
                                                        "PaymentProfileName":"{}".format(paymentpolicy[0]),  
                                                        "PaymentProfileID":"{}".format(paymentId)
                                                        },
                                                        "SellerReturnProfile":{
                                                  
                                                        "ReturnProfileName":"{}".format(returnpolicy[0]),  
                                                        "ReturnProfileID":"{}".format(returnId)
                                                        },
                                                        "SellerShippingProfile":{
                                                      
                                                        "ShippingProfileName": "{}".format(shippingpolicy[0]),
                                                        "ShippingProfileID":"{}".format(shippingId) 
                                                        },
                                        } ,
        
    
                                        
                                        "Site":"US"

                                }
                                        
                
                    }
                    response=api.execute("AddItem", request)
                    print(response.dict())
                    print(response.reply)
                 except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
          

            else:   
                 otherdescriptionFile = open("otherdescription.txt",'r',encoding="utf8")
                 otherdescription=otherdescriptionFile.readlines()
                 product_brand = brand
                 print(categoryID)
                 print(paymentpolicy[0],returnpolicy[0],shippingpolicy[0])
                 print(paymentId,returnId,shippingId)
                 print(category)
              
                 try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "Item":{
                                        "Title":"{}".format(new_title),
                                         "BestOfferDetails":{
                                            "BestOfferEnabled":"true"
                                        },
                                        "Description":"<![CDATA{0}]>".format(otherdescription),
                                        "ListingDuration":"GTC",
                                        "ListingType":"FixedPriceItem",
                                        "Location":"Beverly Hills",
                                        "StartPrice":"{}".format(price),
                                        "Country":"JP",
                                        "Currency":"USD",
                                        "Quantity":"{}".format(count),
                                        "ConditionID":"{}".format(product_state),
                                        "ProductListingDetails":{
                                            "ItemSpecifics":{
                                               "Brand":"CONTINENTAL",
                                               "IncludeeBayProductDetails":"true",
                                               "Mount":"Canon EF",
                                               "Type":"standard"
                                            }
                                                     
                                        },
                                        "ItemSpecifics":{
                                            "NameValueList":{}
                                        },
                                        "PaymentMethods":"PayPal",
                                        "PayPalEmailAddress":"kevinzoo.lancer@gmail.com",
                                        "DispatchTimeMax":"1",
                                        "ShipToLocations":"None",
                                        "ReturnPolicy":{
                                            "ReturnsAcceptedOption":"ReturnsNotAccepted"
                                        },
                                        "PrimaryCategory":{
                                            "CategoryID":"{}".format(categoryID)
                                        },
                                        "PictureDetails":{
                                            "PictureURL":imageurls,
                                        },
                                        "ItemCompatibilityList":{
                                                "Compatibility":{
                                                    "NameValueList":[
                                                        {"Name":"Year","Value":"2010"},
                                                        {"Name":"Make","Value":"Hummer"},
                                                        {"Name":"Model","Value":"H3"}
                                                    ],
                                                    "CompatibilityNotes":"An example compatibility"
                                                }
                                        },
                                      
                                        "SellerProfiles":{

                                                "SellerPaymentProfile":{
                                                   
                                                        "PaymentProfileName":"{}".format(paymentpolicy[0]),  
                                                        "PaymentProfileID":"{}".format(paymentId)
                                                        },
                                                        "SellerReturnProfile":{
                                                  
                                                        "ReturnProfileName":"{}".format(returnpolicy[0]),  
                                                        "ReturnProfileID":"{}".format(returnId)
                                                        },
                                                        "SellerShippingProfile":{
                                                      
                                                        "ShippingProfileName": "{}".format(shippingpolicy[0]),
                                                        "ShippingProfileID":"{}".format(shippingId) 
                                                        },
                                        } ,
        
    
                                        
                                        "Site":"US"

                                }
                                        
                
                    }

                    i=0
                    request['Item']['ItemSpecifics']['NameValueList']={}
                    itemList=[]
                    for item in requiredItems:
                        itemList.append({"Name":item,"Value":requiredValues[i]})
                        i=i+1
                    print(itemList)    
                    request['Item']['ItemSpecifics']['NameValueList']=itemList    
                    response=api.execute("AddItem", request)
                    print(response.dict())
                    print(response.reply)
                 except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass

            
    # get ebay product name list function
    def getProductNameOnEbay (self):
                
                
                try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "ActiveList":{

                                "Include":"true",
                                "Pagination":{
                                    "EntriesPerPage":"50"
                                },
                                "Sort":"CurrentPriceDescending"

                        }
                                        
                    }
                    response=api.execute("GetMyeBaySelling", request)
                    result = response.dict()
                    productlist = result["ActiveList"]["ItemArray"]["Item"]
                    productNameList=[]
                    for product in productlist:
                        productNameList.append(product["Title"])
                    print(productNameList)
                    return productNameList
                    # print(response.reply)
                    # print(response)
                except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
                

      # get ebay product ID list function
    def getProductIDOnEbay (self):

                try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "ActiveList":{

                                "Include":"true",
                                "Pagination":{
                                    "EntriesPerPage":"50"
                                },
                                "Sort":"CurrentPriceDescending"

                        }
                
                    }
                    response=api.execute("GetMyeBaySelling", request)
                    result = response.dict()
                    productlist = result["ActiveList"]["ItemArray"]["Item"]
                    productIdList=[]
                    for product in productlist:
                        productIdList.append(product["ItemID"])
                    print(productIdList)
                    return productIdList
                    # print(response.reply)
                    # print(response)
                except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
                           
    def process_browser_logs_for_network_events(self, logs):
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                    "Network.responseReceived" in log["method"]
            ):
                yield log
    def stop(self):
        # window['console'].update(window['console'].get()+'Ending Scrapper Session~',autoscroll=True)
        self.driver.close()
    
    #translate japanese to english function
    def googletranslate(self,sentence):
        #open new window www.google.com and switch to new window with switch_to.window()
                translate_url = "https://translate.google.ru/?hl=en&tab=rT&sl=ja&tl=en&op=translate"
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.get(translate_url)

                #translate product name from jp into en
                try:
                    translate_source_panel = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"er8xn")))
                except TimeoutException:
                    pass
                print(sentence)
                translate_source_panel.send_keys(sentence)
                time.sleep(5)
                try:
                    translate_target_panel = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"VIiyi")))
                except TimeoutException:
                    pass
                sentence_english = translate_target_panel.text
                print(sentence_english)


                #close window in focus
                self.driver.close()

                #switch abck to old window with switch_to.window()
                self.driver.switch_to.window(self.driver.window_handles[0])    

                return(sentence_english)

    def start(self, url,omitwords,checkgood,checklittle,new,littlenew,bad,bestbad,rating,priceTime,categoryID,paymentpolicy,returnpolicy,shippingpolicy,paymentId,returnId,shippingId,requiredItems,requiredValues):
        ebayProductTitleList = scrap.getProductNameOnEbay()
        ebayProductTitleList=[]
        
        start_url=url
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--disable-extensions')

        driver = webdriver.Chrome(executable_path='./chromedriver',options=chromeOptions)
        self.driver = driver
        self.driver.get(start_url)
        try:
            WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,'js-rapid-override')))
        except TimeoutException:
            pass

        #make image download dirctory named "ProductImageList"
        # image_dirname = "ProductImageList"
        # if not os.path.exists(image_dirname):
        #     os.mkdir(image_dirname)
        # self.don=True
        
            
        state=[]
        omitwords_array=omitwords.split(",")
   
        #get product condition of yahoo
        try:
               
                 if checkgood==True:
                     state.append('目立った傷や汚れなし （詳細）')
                 else:
                     state.append('')
                 if checklittle==True:
                     state.append('やや傷や汚れあり （詳細）')
                 else:
                     state.append('')
                 if new==True:
                     state.append('未使用 （詳細）')
                 else:
                     state.append('')
                 if littlenew==True:
                     state.append('未使用に近い （詳細）')
                 else:
                     state.append('')
                 if bad==True:
                     state.append('傷や汚れあり （詳細）')
                 else:
                     state.append('')
                 if bestbad==True:
                     state.append('全体的に状態が悪い （詳細）')
                 else:
                     state.append('')
                      
                
                
        except TimeoutException:
                pass  
           
        while 1:
            try:
                 WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,'js-rapid-override')))
            except TimeoutException:
                pass
            id=0
            allProducts=self.driver.find_elements_by_class_name("js-rapid-override")
        
            while len(allProducts):
                        
                        print(id)
                        try:
                            WebDriverWait(self.driver,100).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"js-rapid-override")))
                        except TimeoutException:
                            print("timeouterror")
                            pass
                        current_product_count = self.driver.find_elements_by_class_name("js-rapid-override")
                        if id > len(current_product_count):
                            break   
                        self.driver.find_elements_by_class_name("js-rapid-override")[id].click()   
                        print("title")
                        try:
                            WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"ProductTitle__text")))
                        except TimeoutException:
                            pass
                        productTable_div=self.driver.find_element_by_class_name("ProductTable__body").find_element_by_xpath("//th[text()='状態']").find_element_by_xpath("..").find_element_by_tag_name("td").text
                        print(productTable_div)
                        if productTable_div=="未使用 （詳細）":
                            product_state = 1000
                        else:
                            product_state = 3000    
                        if state.count(productTable_div)==0:
                                id=id+2
                                print("this is no")
                                if id==len(allProducts):
                                  self.driver.back()
                                  break
                                self.driver.back()
                                continue
                            
                        #get brand
                        try:
                            productBrand_div=self.driver.find_element_by_class_name("ProductTable__body").find_element_by_xpath("//th[text()='メーカー・ブランド']").find_element_by_xpath("..").find_element_by_tag_name("td").find_element_by_tag_name("a").text
                            print(productBrand_div)
                            brand_english = scrap.googletranslate(productBrand_div)
                            print(brand_english)
                        except:
                           brand_english="No Brand"         
                           pass          
                        
                        #get product category on yahoo
                        category = self.driver.find_element_by_id("yjBreadcrumbs").find_elements_by_tag_name("b")[3]
                        print("this is category",category.text)
                        category_title = category.text            
                        #get product count
                        productCount_div=self.driver.find_element_by_class_name("ProductDetail__items--primary").find_element_by_xpath("//dt[text()='個数']").find_element_by_xpath("..").find_element_by_tag_name("dd").text
                        product_count = productCount_div[1:]
                        print(product_count)
                        
                        try:
                            #find product name
                            WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"ProductTitle__text")))
                            product_title = self.driver.find_element_by_class_name("ProductTitle__text").text 

                            #open new window www.google.com and switch to new window with switch_to.window()
                            translate_url = "https://translate.google.ru/?hl=en&tab=rT&sl=ja&tl=en&op=translate"
                            self.driver.execute_script("window.open('');")
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            self.driver.get(translate_url)

                            #translate product name from jp into en
                            try:
                                translate_source_panel = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"er8xn")))
                            except TimeoutException:
                                pass
                            print(product_title)
                            
                            #remove unnecessary characters
                            # for omitword in omitwords_array:
                            #     print(omitword)
                            #     if product_title.find(omitword)!=-1:
                            #         print("this is exist")
                            #         product_title=product_title.replace(omitword,'')
                            #         print(product_title)


                            

                            translate_source_panel.send_keys(product_title)
                            time.sleep(5)
                            try:
                                translate_target_panel1 = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"VIiyi")))
                            except TimeoutException:
                                pass
                            productName_english = translate_target_panel1.text
                            print(productName_english)
                        
                            #close window in focus
                            self.driver.close()

                            #switch abck to old window with switch_to.window()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                            
                            #processed product title
                            processed_product_title = scrap.processTitle(productName_english,omitwords_array)
                            processed_product_title = processed_product_title.strip()
                            #check if this product is on ebay.
                            if ebayProductTitleList.count(processed_product_title)!=0:
                                id+=2
                                self.driver.back()
                                continue
                        
                           
                            product_price = self.driver.find_element_by_class_name("Price--buynow").find_element_by_class_name("Price__value").text

                            #convert into int 
                            index = product_price.find('円')
                            string_product_price = product_price[0:index]
                            string_product_price=string_product_price.replace(",","")
                            print(string_product_price)
                            int_product_price = int(string_product_price)
                            print(int_product_price)

                            #convert usd dollar of price
                            usd_price = int_product_price*int(rating)/10000
                            usd_price = math.ceil(usd_price)
                            print(usd_price)

                            #up price *
                            up_price = usd_price*float(priceTime)
                            print(up_price)

                        
                            productImageSrcList=[]
                            try:
                                productImageList = WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"ProductImage__link")))
                                image_id=0
                                while(len(productImageList)):
                                    productImage = productImageList[image_id].find_element_by_tag_name("img")
                                    imageSrc = productImage.get_attribute("src")
                                    print(imageSrc)
                                    productImageSrcList.append(imageSrc)
                                
                                    image_id+=1
                                    if image_id == len(productImageList):
                                        break
                            except TimeoutException:    
                                pass
                        except TimeoutException:
                            print("timeout error")
                            pass    
                        
                        #add new product to ebay part
                        scrap.addNewProductOnEbay(omitwords_array,productName_english,up_price,productImageSrcList,product_count,category_title,brand_english,product_state,categoryID,paymentpolicy,returnpolicy,shippingpolicy,paymentId,returnId,shippingId,requiredItems,requiredValues)
                    
                        id=id+2
                        self.driver.back()
                        # self.driver.execute_script("window.history.go(-1)"))
                        if id==len(allProducts):
                            break
            print("this is while")            
            next_div_class_name = ""           
            try:
                next_div_status = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.ID,"ASsp1")))
                # next_div_status = WebDriverWait(self.driver,10).until(EC.visibility_of_all_element_located((By.ID,"ASsp1")))
                next_div = next_div_status.find_elements_by_tag_name("p")[2]
                next_div_class_name = next_div.get_attribute("class")
                print(next_div_class_name)
                # print(next_div)
            except:
                print("this is end") 
                pass    
            if next_div_class_name == "next":
                self.driver.find_element_by_id("ASsp1").find_elements_by_tag_name("p")[2].click()
                print("clicked next button")
                continue
            else:               
                print("not clicked next button")
                break

        messagebox.showinfo("Alert","Successfully listing process end.")
        scrap.stop()

        #start1 function
     
    def __init__(self):
        print("start")

class Register:

      # add new product on ebay function
    def removeProductOnEbay (self,itemid):
            print(itemid)
            id=0    
            try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request={
                        "ItemID":"{}".format(itemid),
                        "EndingReason":"NotAvailable"
                    }
                    response=api.execute("EndFixedPriceItem",request)
                    print(response.dict())
                    print(response.reply)
            except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
    # get ebay product name list function
    def getProductNameOnEbay (self):

                try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "ActiveList":{

                                "Include":"true",
                                "Pagination":{
                                    "EntriesPerPage":"50"
                                },
                                "Sort":"CurrentPriceDescending"

                        }
                                        
                    }
                    response=api.execute("GetMyeBaySelling", request)
                    result = response.dict()
                    productlist = result["ActiveList"]["ItemArray"]["Item"]
                    productNameList=[]
                    for product in productlist:
                        productNameList.append(product["Title"])
                    print(productNameList)
                    return productNameList
                    # print(response.reply)
                    # print(response)
                except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
                

      # get ebay product ID list function
    def getProductIDOnEbay (self):

                try:    
                    api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                    request = {
                        "ActiveList":{

                                "Include":"true",
                                "Pagination":{
                                    "EntriesPerPage":"50"
                                },
                                "Sort":"CurrentPriceDescending"

                        }
                
                    }
                    response=api.execute("GetMyeBaySelling", request)
                    result = response.dict()
                    productlist = result["ActiveList"]["ItemArray"]["Item"]
                    productIdList=[]
                    for product in productlist:
                        productIdList.append(product["ItemID"])
                    print(productIdList)
                    return productIdList
                    # print(response.reply)
                    # print(response)
                except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    pass
                           
    def process_browser_logs_for_network_events(self, logs):
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                    "Network.responseReceived" in log["method"]
            ):
                yield log
    def stop(self):
        # window['console'].update(window['console'].get()+'Ending Scrapper Session~',autoscroll=True)
        self.driver.close()
    
    #translate japanese to english function
    def googletranslate(self,sentence):
        #open new window www.google.com and switch to new window with switch_to.window()
                translate_url = "https://translate.google.ru/?hl=en&tab=rT&sl=ja&tl=en&op=translate"
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.get(translate_url)

                #translate product name from jp into en
                try:
                    translate_source_panel = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"er8xn")))
                except TimeoutException:
                    pass
                print(sentence)
                translate_source_panel.send_keys(sentence)
                time.sleep(5)
                try:
                    translate_target_panel = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"VIiyi")))
                except TimeoutException:
                    pass
                sentence_english = translate_target_panel.text
                print(sentence_english)


                #close window in focus
                self.driver.close()

                #switch abck to old window with switch_to.window()
                self.driver.switch_to.window(self.driver.window_handles[0])    

                return(sentence_english)

    def remove(self, url,omitwords,checkgood,checklittle,new, littlenew,bad,bestbad):
        ebayProductTitleList = scrap.getProductNameOnEbay()
        
        start_url=url
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        chromeOptions = Options()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--disable-extensions')

        driver = webdriver.Chrome(executable_path='./chromedriver',options=chromeOptions)
        self.driver = driver
        self.driver.get(url)

        #make csv file
        # df = pd.DataFrame()
        # file_url = 'product_list.csv'
        # #maximize browser
        # self.driver.maximize_window()
        try:
            WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,'js-rapid-override')))
        except TimeoutException:
            pass

        #make image download dirctory named "ProductImageList"
        
       
           
        state=[]
        omitwords_array=omitwords.split(",")

        #get product condition of yahoo
        try:
               
                if checkgood==True:
                     state.append('目立った傷や汚れなし （詳細）')
                else:
                     state.append('')
                if checklittle==True:
                     state.append('やや傷や汚れあり （詳細）')
                else:
                     state.append('')
                if new==True:
                     state.append('未使用 （詳細）')
                else:
                     state.append('')
                if littlenew==True:
                     state.append('未使用に近い （詳細）')
                else:
                     state.append('')
                if bad==True:
                     state.append('傷や汚れあり （詳細）')
                else:
                     state.append('')
                if bestbad==True:
                     state.append('全体的に状態が悪い （詳細）')
                else:
                     state.append('')
                
        except TimeoutException:
                pass  
        while 1:
                try:
                   WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.CLASS_NAME,'js-rapid-override')))
                except TimeoutException:
                   pass
                id=98
                allProducts=self.driver.find_elements_by_class_name("js-rapid-override")
                print("aaa")
                while len(allProducts):
                    product = allProducts[id]
                    print(product)
                    print(id)
                    try:
                        WebDriverWait(self.driver,200).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"js-rapid-override")))
                    except TimeoutException:
                        print("timeouterror")
                        pass   
                    self.driver.find_elements_by_class_name("js-rapid-override")[id].click()   
                    print("title")
                    try:
                       WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"ProductTitle__text")))
                    except TimeoutException:
                        pass
                    productTable_div=self.driver.find_element_by_class_name("ProductTable__body").find_element_by_xpath("//th[text()='状態']").find_element_by_xpath("..").find_element_by_tag_name("td").text
                    print(productTable_div)
                    if state.count(productTable_div)==0:
                            id=id+2
                            print("this is no")
                            if id==len(allProducts):
                              self.driver.back()
                              break
                            self.driver.back()
                            continue
                        
                
                                
                    #get product count
                    productCount_div=self.driver.find_element_by_class_name("ProductDetail__items--primary").find_element_by_xpath("//dt[text()='個数']").find_element_by_xpath("..").find_element_by_tag_name("dd").text
                    product_count = productCount_div[1:]
                    print(product_count)
                    
                    try:
                        #find product name
                        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"ProductTitle__text")))
                        product_title = self.driver.find_element_by_class_name("ProductTitle__text").text 

                        #open new window www.google.com and switch to new window with switch_to.window()
                        translate_url = "https://translate.google.ru/?hl=en&tab=rT&sl=ja&tl=en&op=translate"
                        self.driver.execute_script("window.open('');")
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        self.driver.get(translate_url)

                        #translate product name from jp into en
                        try:
                            translate_source_panel = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"er8xn")))
                        except TimeoutException:
                            pass
                        print(product_title)
                        


                        translate_source_panel.send_keys(product_title)
                        time.sleep(10)
                        try:
                            translate_target_panel1 = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME,"VIiyi")))
                        except TimeoutException:
                            pass
                        productName_english = translate_target_panel1.text
                        print(productName_english)
                        productName_english = scrap.processTitle(productName_english,omitwords_array)
                        #close window in focus
                        self.driver.close()

                        #switch abck to old window with switch_to.window()
                        self.driver.switch_to.window(self.driver.window_handles[0])

                        #get product count
                        try:  
                            productCount_div=self.driver.find_element_by_class_name("ProductDetail__items--primary").find_element_by_xpath("//dt[text()='個数']").find_element_by_xpath("..").find_element_by_tag_name("dd").text
                            product_count = productCount_div[1:]
                            print(product_count)
                        except:
                            pass
                        productName_english = productName_english.strip()
                        print("this is productname:",productName_english)
                        #check if this product is on ebay.
                        if  ebayProductTitleList.count(productName_english)==0:
                            print("there is no product like this title")
                            id+=2
                            self.driver.back()
                            continue
                        if product_count=='0':
                            productNameListOnEbay = scrap.getProductNameOnEbay()
                            productIdListOnEbay = scrap.getProductIDOnEbay()
                            product_index = productNameListOnEbay.index(productName_english)                
                            product_id = productIdListOnEbay[product_index]
                            print("this is remove product id",product_id)
                            register.removeProductOnEbay(product_id)

                    except TimeoutException:
                        print("timeout error")
                        pass    
                    
                    
                
                    id=id+2
                    self.driver.back()
                    if id==len(allProducts):
                        break


                print("this is while")            
                next_div_class_name = ""           
                try:
                    next_div_status = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.ID,"ASsp1")))
                    # next_div_status = WebDriverWait(self.driver,10).until(EC.visibility_of_all_element_located((By.ID,"ASsp1")))
                    next_div = next_div_status.find_elements_by_tag_name("p")[2]
                    next_div_class_name = next_div.get_attribute("class")
                    print(next_div_class_name)
                    # print(next_div)
                except:
                 
                    pass    
                if next_div_class_name == "next":
                    self.driver.find_element_by_id("ASsp1").find_elements_by_tag_name("p")[2].click()
                    continue
                else:               
                    break
        messagebox.showinfo("Alert","Successfully remove process end.")
        register.stop()

        

    def __init__(self):
            print("remove product that have no count")

if __name__ == "__main__":
     
    
  
    scrap = ScrapePlaces()
    register = Register()
    omitwordFile = open("omitwords.txt",'r',encoding="utf8")
    omitwords = omitwordFile.read()
    categoryFile = open("category.txt","r")
    categoryList = categoryFile.readlines()
    categoryDB = []
    # for category in categoryList:
    #     itemArray = category.split("+")
    #     levelArray = itemArray[0].split(" ")
    #     categoryArray = itemArray[1].split("=")
    #     parentIDArray = itemArray[2].split("=")
    #     categoryName = categoryArray[0].strip()
    #     print(levelArray[1],categoryName,categoryArray[1],parentIDArray[1])
    #     categoryDB.append([levelArray[1],categoryName,categoryArray[1],parentIDArray[1]])

    database = r".\sqllite\ebay.db"
    # scores = [[1,"Buddy Rich1", 1,101], [1,"Candido1",1, 91], [1,"Charlie Byrd1",1,81]]
    con = sqlite3.connect(database)
  
    cursor = con.cursor()
    sqlite_select_query = """SELECT * from category1 WHERE level=1"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print("Total rows are:  ", len(records))
    print("Printing each row")
    category1 = []
    category2 = []
    category3 = []
    category4 = []
    category5 = []
    category6 = []
    for row in records:
        category1.append(row[2])

    api = Policies(domain='svcs.ebay.com',config_file='ebay.yaml')
    res = api.execute('getSellerProfiles')
    result = res.dict()
    paymentProfiles = result['paymentProfileList']['PaymentProfile']
    returnProfiles = result['returnPolicyProfileList']['ReturnPolicyProfile']
    shippingProfiles = result['shippingPolicyProfile']['ShippingPolicyProfile']
    paymentlist = []
    returnlist = []
    shippinglist = []
    paymentID = []
    returnID = []
    shippingID = []
    for payment in paymentProfiles:
        paymentlist.append(payment['profileName'])
        paymentID.append(payment['profileId'])
    for returnPolicy in returnProfiles:
        returnlist.append(returnPolicy['profileName'])
        returnID.append(returnPolicy['profileId'])
    for shipping in shippingProfiles:
        shippinglist.append(shipping['profileName'])
        shippingID.append(shipping['profileId']) 
    print(paymentlist,returnlist,shippinglist)
   
    layout =[

            [sg.Text('入力URL:',size=(17,1)),sg.Input(default_text = "https://auctions.yahoo.co.jp/seller/crash6159?", size=(90, 1), key='url')],
            [sg.Text('省略単語:',size=(17,1)),sg.Multiline(size=(88,10),key='omitwords',default_text=omitwords)],
            [sg.Text('抽出商品状態:',size=(17,1)),sg.Checkbox('未使用',size=(10,1),key='new'),sg.Checkbox('未使用に近い',size=(10,1),key='littlenew'),sg.Checkbox('目立った傷や汚れなし',size=(10,1),key='checkgood'),sg.Text("",size=(5,1)),sg.Text("為替レート:１万円:",size=(10,1)),sg.Input(size=(10,1),default_text="80",key='rating'),sg.Text("$")],
            [sg.Text('',size=(17,1)),sg.Checkbox('やや傷や汚れあり',size=(10,1),key='checklittle'),sg.Checkbox('傷や汚れあり',size=(10,1),key='bad'),sg.Checkbox('全体的に状態が悪い',size=(10,1),key='bestbad'),sg.Text("",size=(5,1)),sg.Text("価格改定：",size=(10,1)),sg.Input(size=(10,1),default_text="1.5",key='priceTime')],
            [sg.Text("商品カテゴリを選択してください")],
            [sg.Listbox(category1, size=(15, 10),key='category1', enable_events=True,),sg.Listbox(category2, size=(15, 10),key='category2', enable_events=True),sg.Listbox(category3, size=(15, 10),key='category3', enable_events=True),sg.Listbox(category4, size=(15, 10),key='category4', enable_events=True),sg.Listbox(category5, size=(15, 10),key='category5', enable_events=True),sg.Listbox(category6, size=(15, 10),key='category6', enable_events=True)],
            [sg.Text("ビジネスポリシーを選択してください")],
            [sg.Text("Payment Policy", size=(15,1)),sg.Text("Return Policy",size=(15,1)),sg.Text("Shipping Policy")],
            [sg.Listbox(paymentlist, size=(15, 5),key='paymentlist', enable_events=True,),sg.Listbox(returnlist, size=(15, 5),key='returnlist', enable_events=True),sg.Listbox(shippinglist, size=(15, 5),key='shippinglist', enable_events=True)],
            [sg.Text('',size=(55,1)),sg.Button('Start',size=(10,1)),  sg.Button('Stop',size=(10,1)), sg.Button('Omitwords Save',size=(15,1))],
            [sg.Text('',size=(55,1)),sg.Text("在庫管理")],
            [sg.Text('',size=(55,1)),sg.Button('Remove',size=(10,1)),  sg.Button('RemoveStop',size=(10,1))]
 
    ]

    window = sg.Window('Yahoo Product Extract',layout)
    checkformflag1=True
    checkformflag2=True
    checkformflag3=True
    checkformflag4=True
    checkformflag5=True
    productCategoryID=0
    checkPayment=False
    checkReturn=False
    checkShipping=False
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
       

        if event =='category1' and values['category1'] != '':
            print(values['category1'][0])
            categoryName1=values['category1'][0]
            quotoIndex = categoryName1.find("'")
            if quotoIndex!=-1:
                    categoryName1 = categoryName1.replace("'","''")
                    print(categoryName1)
            category2 = []
            sqlite_select_query = """SELECT category_id from category1 WHERE category_name="""+"'"+categoryName1+"'"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print(records[0][0])
            category_id1 = records[0][0]
            productCategoryID = records[0][0]
            print("prodcut",productCategoryID)
            query1 = """select * from category1 where parent_id=""" + "'" + str(category_id1) + "'" +  """and level!=1"""
            cursor.execute(query1)
            records = cursor.fetchall()
           
            for row in records:
               category2.append(row[2])
            print(category2)   
            window['category2'].update(category2)
        if event =='category2' and values['category2'] != '':
            print(values['category2'][0])
            categoryName2=values['category2'][0]
            quotoIndex = categoryName2.find("'")
            if quotoIndex!=-1:
                    categoryName2 = categoryName2.replace("'","''")
                    print(categoryName2)
            category3 = []
            sqlite_select_query = """SELECT category_id from category1 WHERE category_name="""+"'"+categoryName2 +"'"
            # try:
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print(records[0][0])
            category_id2 = records[0][0]
            productCategoryID = records[0][0]
            print("prodcut",productCategoryID)
            query1 = """select * from category1 where parent_id=""" + "'" + str(category_id2) + "'" +  """and level!=2"""
            cursor.execute(query1)
            records = cursor.fetchall()
            for row in records:
                 category3.append(row[2])
                 print(category3)   
            # except:
            #     pass
            
            window['category3'].update(category3)
        if event =='category3' and values['category3'] != '':
                print(values['category3'][0])
                categoryName3=values['category3'][0]
                quotoIndex = categoryName3.find("'")
                if quotoIndex!=-1:
                    categoryName3 = categoryName3.replace("'","''")
                    print(categoryName3)
                category4 = []
                sqlite_select_query = """SELECT category_id from category1 WHERE category_name="""+"'"+categoryName3 +"'"
    #   ?      try:
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                print(records[0][0])
                category_id3 = records[0][0]
                productCategoryID = records[0][0]
                query1 = """select * from category1 where parent_id=""" + "'" + str(category_id3) + "'" +  """and level!=2"""
                cursor.execute(query1)
                records = cursor.fetchall()
           
                for row in records:
                    category4.append(row[2])
                    print(category4)   
            # except:
            #     pass
                window['category4'].update(category4)
        if event =='category4' and values['category4'] != '':
                print(values['category4'][0])
                categoryName4=values['category4'][0]
                quotoIndex = categoryName4.find("'")
                if quotoIndex!=-1:
                    categoryName4 = categoryName4.replace("'","''")
                    print(categoryName4)
                category5 = []
                sqlite_select_query = """SELECT category_id from category1 WHERE category_name="""+"'"+categoryName4 +"'"
            # try:
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                print(records[0][0])
                productCategoryID = records[0][0]
                print("prodcut",productCategoryID)
                category_id4 = records[0][0]
                query1 = """select * from category1 where parent_id=""" + "'" + str(category_id4) + "'" +  """and level!=2"""
                cursor.execute(query1)
                records = cursor.fetchall()
           
                for row in records:
                    category5.append(row[2])
                    print(category5)   
            # except:
            #     pass
                window['category5'].update(category5)
            
        if event =='category5' and values['category5'] != '':
                print(values['category5'][0])
                categoryName5=values['category5'][0]
                quotoIndex = categoryName5.find("'")
                if quotoIndex!=-1:
                    categoryName5 = categoryName5.replace("'","''")
                    print(categoryName5)
                category6 = []
                sqlite_select_query = """SELECT category_id from category1 WHERE category_name="""+"'"+categoryName5 +"'"
            # try:
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                print(records[0][0])
                category_id5 = records[0][0]
                productCategoryID = records[0][0]
                print("prodcut",productCategoryID)
                query1 = """select * from category1 where parent_id=""" + "'" + str(category_id5) + "'" +  """and level!=2"""
                cursor.execute(query1)
                records = cursor.fetchall()
           
                for row in records:
                    category6.append(row[2])
                    print(category6)   
            # except:
            #     pass
                window['category6'].update(category6)    

        if event =='category6' and values['category6'] != '':
                print(values['category6'][0])
                categoryName6=values['category6'][0]
                quotoIndex = categoryName6.find("'")
                if quotoIndex!=-1:
                    categoryName6 = categoryName6.replace("'","''")
                    print(categoryName6)
                category6 = []
                sqlite_select_query = """SELECT category_id from category1 WHERE category_name="""+"'"+categoryName6 +"'"
            # try:
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                print(records[0][0])
                category_id6 = records[0][0]
                productCategoryID = records[0][0]
                print("prodcut",productCategoryID)
                
                window['category6'].update(category6)    
        elif event == "Omitwords Save":
            scrap.omitwordSave(values['omitwords'])

        elif event == "Start":
            print("product",productCategoryID)
            query1 = """select * from category1 where parent_id=""" + "'" + str(productCategoryID) + "'"
            cursor.execute(query1)
            records = cursor.fetchall()
            print(records)
            print(values['paymentlist'])
            print(values['returnlist'])
            print(values['shippinglist'])
            if records==[] and productCategoryID!=0:
                        if values['paymentlist'] != []:
                           checkPayment = True
                        else:
                          messagebox.showinfo("Alert","Please select payment policy")  
               
                        if  values['returnlist'] != []:
                           checkReturn = True
                        else:
                          messagebox.showinfo("Alert","Please select return policy")  

                        if values['shippinglist'] != []:
                           checkShipping = True
                        else:
                          messagebox.showinfo("Alert","Please select shipping policy") 


                        if values['url'] == '':
                            messagebox.showinfo("Alert","Please input Target Url")
                            checkformflag1=False
                        else: 
                            checkformflag1=True
                        if values['omitwords']=='':
                            messagebox.showinfo("Alert","Please input omitwords")
                            checkformflag2=False
                        else:
                            checkformflag2=True
                        
                        if values['checkgood']==False| values['checklittle']==False|values['new']==False| values['littlenew']==False|values['bad']==False| values['bestbad']==False:
                            messagebox.showinfo('Alert','Please check production condition') 
                            checkformflag3=False
                        else:
                            checkformflag3=True
                        if values['rating']=='':
                            messagebox.showinfo('Alert',"Please input exchange rating")
                            checkformflag4=False
                        else:
                            checkformflag4=True
                        if values['priceTime']=='':
                            messagebox.showinfo("Alert","Please input Price Time")   
                            checkformflag5=False
                        else:
                            checkformflag5=True
                        if checkformflag1==True&checkformflag2==True&checkformflag3==True&checkformflag4==True&checkformflag5==True&checkPayment==True&checkReturn==True&checkShipping==True:
                            api = Trading(domain='api.ebay.com',config_file='ebay.yaml',siteid=0)
                            request = {
                                    "CategorySpecific":{
                                        "CategoryID":"{}".format(productCategoryID)
                                    }

                                }
                            try:         
                                response=api.execute("GetCategorySpecifics", request)
                                # print(response.dict())
                            except:
                                messagebox.showinfo("Error","Please choose correct category")
                                pass
                            result = response.dict()
                            requiredItems = []
                            requiredNames = []
                            for item in result['Recommendations']['NameRecommendation']:
                                if item['ValidationRules']['UsageConstraint'] == 'Required':
                                    print(item['Name'])
                                    print(item['ValueRecommendation'][0]['Value'])
                                    requiredItems.append(item['Name'])
                                    requiredNames.append(item['ValueRecommendation'][0]['Value'])
                            paymentIndex = paymentlist.index(values['paymentlist'][0])
                            returnIndex = returnlist.index(values['returnlist'][0])
                            shippingIndex = shippinglist.index(values['shippinglist'][0])
                            paymentId = paymentID[paymentIndex]
                            returnId = returnID[returnIndex]
                            shippingId = shippingID[shippingIndex]
                            threading.Thread(target=scrap.start, args=(values['url'],values['omitwords'],values['checkgood'],values['checklittle'],values['new'],values['littlenew'],values['bad'],values['bestbad'],values['rating'],values['priceTime'],productCategoryID,values['paymentlist'],values['returnlist'],values['shippinglist'],paymentId,returnId,shippingId,requiredItems, requiredNames), daemon=True).start()
                            window.FindElement('Start').Update(disabled=True)
            else:
                messagebox.showinfo("Error","Please select correct category")  
           
        elif event == "Stop":
            window.FindElement('Start').Update(disabled=False)
            scrap.stop()
        elif event == "Remove":
            if values['url'] == '':
                messagebox.showinfo("Alert","Please input Target Url")
                checkformflag1=False
            else: 
                checkformflag1=True
            if values['omitwords']=='':
                messagebox.showinfo("Alert","Please input omitwords")
                checkformflag2=False
            else:
                checkformflag2=True
            
            if values['checkgood']==False| values['checklittle']==False|values['new']==False| values['littlenew']==False|values['bad']==False| values['bestbad']==False:
                messagebox.showinfo('Alert','Please check production condition') 
                checkformflag3=False
            else:
                checkformflag3=True
           
            if checkformflag1==True&checkformflag2==True&checkformflag3==True&checkformflag4==True&checkformflag5==True:
               threading.Thread(target=register.remove,args=(values['url'],values['omitwords'],values['checkgood'],values['checklittle'],values['new'],values['littlenew'],values['bad'],values['bestbad'],),daemon=True).start()
               window.FindElement("Remove").Update(disabled=True)

        elif event == "RemoveStop":
                window.FindElement('Remove').Update(disabled=False)
                register.stop()


    window.close()

