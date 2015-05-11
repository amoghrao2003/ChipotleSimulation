__author__ = 'voldy'


import threading
import Queue
import time, random
import json
import unirest
import pymysql
#import requests
# change the no of people adding bhaji after asking customer.
# we have only one now, we can change
WORKERS = 1

# Create thread class
class Worker(threading.Thread):

    # constructor
    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)
        self.connection = pymysql.connect("dbinstance-sjsu-amogh.cyht8ykut6xk.us-west-1.rds.amazonaws.com","voldy","voldysjsu","cmpe275")


    def run(self):
        print "Meat Worker Listening"
        while 1:
         #   print  "Hey Im working: MeatWorker"

            #Keep listening there is no customer yet in store
            if meatQueue.empty():
                #Chill
                time.sleep(random.randint(10, 100) / 50.0)
                continue
            else:
                #Hey there is a Customer in my shop.
                item = self.__queue.get()
                #parse to get Customer Info
                customer_channel = parseInfo(item)
                print "Connecting to "+customer_channel

                print "Asking Customer (Chicken/Beef/Pork)"
                #Lets ask him his requirements Burrito/Bowl
                responseMeat = unirest.get("http://"+customer_channel+"/getMeat", headers={ "Accept": "application/json" },
                                       params={ "meat": "Chicken/Beef/Pork" })

                #If customer replies with his choice, Process order and send to next worker
                if responseMeat.code==200:
                    meatValue = responseMeat._body
                    print "I will add Delicious "+responseMeat.body+" for you !"


                print "Asking Customer (Pinto/Black Beans)"
                #Lets ask user which type of Rice he wants.
                responseBeans = unirest.get("http://"+customer_channel+"/getBeans", headers={ "Accept": "application/json" },
                                       params={ "beans": "Pinto,Black" })

                #If customer replies with his choice, Process order and send to next worker
                if responseBeans.code==200:
                    print "I will add Delicious "+responseBeans.body+" for you !"
                    beanValue = responseBeans.body
                    self.cursor = self.connection.cursor()
                    self.cursor.execute("UPDATE  Orders SET Stage ='{0}' WHERE CustomerName = '{1}'".format("2",parseCustomerInfo(item)))
                    self.connection.commit()
                    self.cursor.close()
                    sendToNextWorker(item,meatValue,beanValue)





meatQueue = Queue.Queue(0)



def startWorker():
    print  "Start Worker Thread"
    Worker(meatQueue).start()



def parseInfo(item):
    print item
    data = json.loads(item)
   # data = requests.get(item).json()
    print data['clientChannel']
    return data['clientChannel']

def parseCustomerInfo(item):
    data = json.loads(item)
    return data['customerName']

def sendToNextWorker(item,meatValue,beanValue):
    data = json.loads(item)
    data["meat"] = meatValue
    data["bean"] = beanValue
    datadumps = json.dumps(data)
    customer_channel = parseInfo(item)

    print  "Send to SauceWorker:"
    #Send to next worker
    response = unirest.post("http://localhost:8082/send", headers={"Accept": "application/json"},
                            params=datadumps)

    #print response.code
    return response

    #return data



