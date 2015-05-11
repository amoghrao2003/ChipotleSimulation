__author__ = 'Abhinav'

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
        print "Cashier Worker Listening"

        while 1:
           # print  "Hey Im working"

            #Keep listening there is no customer yet in store
            if billQueue.empty():
                #Chill
                time.sleep(random.randint(10, 100) / 50.0)
                continue
            else:
                #Hey there is a Customer in my shop.
                item = self.__queue.get()

                #parse to get Customer Info
                customer_channel = parseInfo(item)
                print "Connecting to "+customer_channel

                print "telling customer his total bill amount"
                #print "Asking Customer if he wants any drink"
                #Lets ask him his requirements about Drink


                total = calculateCost(item)
                response=sendToCustomer(item,total)
            if response.code==200:
                    print "Amount received: "+response.body
                    self.cursor = self.connection.cursor()
                    self.cursor.execute("UPDATE  Orders SET Stage ='{0}' WHERE CustomerName = '{1}'".format("5",parseCustomerInfo(item)))
                    self.connection.commit()
                    self.cursor.close()

'''
                response = unirest.get("http://"+customer_channel+"/getBase", headers={ "Accept": "application/json" },
                                       params={ "TotalBill": "Burrito/Bowl" })
                #If customer replies with his choice, Process order and send to next worker
                if response.code==200:
                    print "I will add Delicious "+response.body+" for you !"
                    sendToNextWorker(item,response.body)

'''


billQueue = Queue.Queue(0)


#this will come for each customer . below consider that 1-5 customer made a rest call of their choices.
# all should be added in queue. worker works on the queue
# we will add in queue as soon as we get request from neighbouring worker

# Create a Worker whose work is to add bhaji. the bhaji he has to add will be in Queue
#This guy will listen to Queue


def startWorker():
    print  "Start Worker Thread"
    Worker(billQueue).start()


def calculateCost(item):
    cost=0
    data = json.loads(item)

    if(data['base']=='Burrito'):
        cost=5

    return cost

def parseInfo(item):
    data = json.loads(item)
    return data['clientChannel']

def parseCustomerInfo(item):
    data = json.loads(item)
    return data['customerName']

def sendToCustomer(item,cost):
    data = json.loads(item)
    data["total"] = cost
    datadumps = json.dumps(data)
    customer_channel = parseInfo(item)
    #print "datadumps ::" + datadumps
    print  "Send Base to MeatWorker:"
    #Send to next worker
    response = unirest.post("http://"+customer_channel+"/sendBill", headers={"Accept": "application/json"},
                            params=datadumps)
    print response.code
    return response



