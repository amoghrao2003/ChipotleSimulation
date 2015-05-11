__author__ = 'voldy'


import threading
import Queue
import time, random
import json
import unirest
import pymysql
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
        print "Base Worker Listening"

        while 1:
           # print  "Hey Im working"

            #Keep listening there is no customer yet in store
            if orderQueue.empty():
                #Chill
                time.sleep(random.randint(10, 100) / 50.0)
                continue
            else:
                #Hey there is a Customer in my shop.
                item = self.__queue.get()




                #parse to get Customer Info
                customer_channel = parseInfo(item)
                print "Connecting to "+customer_channel

                print "Asking Customer (Tortilla/Bowl)"
                #Lets ask him his requirements Burrito/Bowl
                responseBase = unirest.get("http://"+customer_channel+"/getBase", headers={ "Accept": "application/json" },
                                       params={ "base": "Tortilla/Bowl" })

                #If customer replies with his choice, Process order and send to next worker
                if responseBase.code==200:
                    print "I will add Delicious "+responseBase.body+" for you !"
                    baseValue = responseBase.body

                print "Asking Customer (Brown/White Rice)"
                #Lets ask user which type of Rice he wants.
                responseRice = unirest.get("http://"+customer_channel+"/getRice", headers={ "Accept": "application/json" },
                                       params={ "rice": "Brown,White" })

                #If customer replies with his choice, Process order and send to next worker
                if responseRice.code==200:
                    print "I will add Delicious "+responseRice.body+" for you !"
                    self.cursor = self.connection.cursor()
                    self.cursor.execute("INSERT INTO Orders(CustomerName, Stage ) VALUES ( '{0}', '{1}')".format(parseCustomerInfo(item),"1"))
                    self.connection.commit()
                    self.cursor.close()
                    riceValue = responseRice.body
                    sendToNextWorker(item,baseValue,riceValue)

orderQueue = Queue.Queue(0)

def startWorker():
    print  "Start Worker Thread"
    Worker(orderQueue).start()


'''
#end kaam
for i in range(WORKERS):
    orderQueue.put(None) # add end-of-queue markers

'''

def parseInfo(item):
    data = json.loads(item)
    return data['clientChannel']

def parseCustomerInfo(item):
    data = json.loads(item)
    return data['customerName']

def sendToNextWorker(item,baseValue,riceValue):
    data = json.loads(item)
    data["base"] = baseValue
    data["rice"] = riceValue
    datadumps = json.dumps(data)
    customer_channel = parseInfo(item)

    print  "Send to MeatWorker:"
    #Send to next worker
    response = unirest.post("http://localhost:8081/send", headers={"Accept": "application/json"},
                            params=datadumps)
    #print response.code
    return response



