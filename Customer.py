__author__ = 'voldy'


from bottle import request,route,static_file,run
import json
import unirest
import random

@route('/getBase', method='GET')
def getBase():
    Base = ['Burrito', 'Bowl']
    print "I would Like to have " + random.choice(Base)
    return random.choice(Base)

@route('/getMeat', method='GET')
def getMeat():
    Meat = ['Chicken','Pork', 'Beef']
    print "I would Like to have " + random.choice(Meat)
    return random.choice(Meat)

@route('/getRice', method='GET')
def getRice():
    rice = ['Brown Rice','White Rice']
    print "I would Like to have " + random.choice(rice)
    return random.choice(rice)

@route('/getBeans', method='GET')
def getBeansi():
    beans = ['Pinto', 'Black Beans']
    print "I would Like to have " + random.choice(beans)
    return random.choice(beans)

@route('/getSauce', method='GET')
def getSauce():
    sauce = ['Corn Sauce','Mayo', 'Salsa Sauce','Red sauce']
    print "I would have " + random.choice(sauce)
    return random.choice(sauce)

@route('/getGarnish', method='GET')
def getSauce():
    garnish = ['Cheese','Guacamole','Lettuce']
    print "I would have " + random.choice(garnish)
    return random.choice(garnish)

@route('/sendBill', method='POST')
def sendBill():
    print "Customer reviews the bill"
    bill=request._get_body_string()
    print "Bill is", bill
    payBill(bill)
    #print bill
    return "bill received"

def payBill(bill):
    data = json.loads(bill)
    amount = data["total"]
    payMethod = "Credit Card"

    paymentDict = {'amount':amount,
                   'paymentMethod':payMethod}

    #Pay Bill
    response = unirest.post("http://localhost:8084/payBill", headers={"Accept": "application/json"},
                            params=paymentDict)

    if response.code==200:
        print "Thanks for the Burrito!"


def initiateRequest():
        customerInfo = '{"clientChannel":"localhost:9080","customerName":"Salman"}'

        #Initiate
        response = unirest.post("http://localhost:8080/markPresence", headers={"Accept": "application/json"},
                            params=customerInfo)




if __name__ == '__main__':
    initiateRequest()
    run(host='localhost',port =9080)
