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
        print "Sauce Worker Listening"
        while 1:
         #   print  "Hey Im working: MeatWorker"

            #Keep listening there is no customer yet in store
            if sauceQueue.empty():
                #Chill
                time.sleep(random.randint(10, 100) / 50.0)
                continue
            else:
                #Hey there is a Customer in my shop.
                item = self.__queue.get()
                #parse to get Customer Info
                customer_channel = parseInfo(item)
                print "Connecting to "+customer_channel

                print "Asking Customer (Corn/Mayo/Salsa/Red sauce)"
                #Lets ask him his requirements Burrito/Bowl
                responseSauce = unirest.get("http://"+customer_channel+"/getSauce", headers={ "Accept": "application/json" },
                                       params={ "sauce": "Corn/Mayo/Salsa/Red sauce" })
                #If customer replies with his choice, Process order and send to next worker
                if responseSauce.code==200:
                    sauceValue = responseSauce._body
                    print "I will add Delicious "+responseSauce.body+" for you !"
                    self.cursor = self.connection.cursor()
                    self.cursor.execute("UPDATE  Orders SET Stage ='{0}' WHERE CustomerName = '{1}'".format("3",parseCustomerInfo(item)))
                    self.connection.commit()
                    self.cursor.close()
                    sendToNextWorker(item,sauceValue)





sauceQueue = Queue.Queue(0)



def startWorker():
    print  "Start Worker Thread"
    Worker(sauceQueue).start()



def parseInfo(item):
    print item
    data = json.loads(item)
   # data = requests.get(item).json()
    print data['clientChannel']
    return data['clientChannel']

def parseCustomerInfo(item):
    data = json.loads(item)
    return data['customerName']

def sendToNextWorker(item,sauceValue):
    data = json.loads(item)
    data["sauce"] = sauceValue

    datadumps = json.dumps(data)
    customer_channel = parseInfo(item)

    print  "Send to GarnishWorker:"
    #Send to next worker
    response = unirest.post("http://localhost:8083/send", headers={"Accept": "application/json"},
                            params=datadumps)
    #print response.code
    return response

    #return data



