__author__ = 'Abhinav'

import threading
import Queue
import time, random
import json
import unirest
# change the no of people adding bhaji after asking customer.
# we have only one now, we can change
WORKERS = 1


# Create thread class
class Worker(threading.Thread):
    orderNumber=1
    # constructor
    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)


    def run(self):
        print "Base Worker Listening"
        capacity=0
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

                print "Asking Customer (Burrito/Bowl)"
                #Lets ask him his requirements Burrito/Bowl

                response = unirest.get("http://"+customer_channel+"/getBase", headers={ "Accept": "application/json" },
                                       params={ "base": "Burrito/Bowl" })
                #If customer replies with his choice, Process order and send to next worker
                if response.code==200:
                    print capacity
                    if capacity==0:
                        print "Kindly give me a minute so that I can refill the vessel"
                        #code to refill - a rest call
                        capacity=2

                    print "I will add Delicious "+response.body+" for you !"
                    capacity=capacity-1
                    sendToNextWorker(item,response.body)

orderQueue = Queue.Queue(0)

#this will come for each customer . below consider that 1-5 customer made a rest call of their choices.
# all should be added in queue. worker works on the queue
# we will add in queue as soon as we get request from neighbouring worker

'''
customer_veggie_choice = ["tamatar-customr1","kanda-customr2","mirchi-customr3","aalo-customr4","batata-customr5"]

for i in customer_veggie_choice:
        orderQueue.put(i)
'''

# Create a Worker whose work is to add bhaji. the bhaji he has to add will be in Queue
#This guy will listen to Queue

'''
for i in range(WORKERS):
    Worker(orderQueue).start() # start a worker
'''


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

def sendToNextWorker(item,baseChoice):
    data = json.loads(item)
    data["orderNumber"] = self.orderNumber
    data["base"] = baseChoice
    datadumps = json.dumps(data)
    customer_channel = parseInfo(item)
    print "datadumps ::" + datadumps
    print  "Send Base to MeatWorker:"
    #Send to next worker
    response = unirest.post("http://localhost:8081/sendBase", headers={"Accept": "application/json"},
                            params=datadumps)
    print response.code
    return response



