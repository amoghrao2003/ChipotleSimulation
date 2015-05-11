__author__ = 'voldy'


from bottle import request,route,static_file,run
import json
import unirest

@route('/getBase', method='GET')
def getBase():
    print "I would Like to have Burrito"
    return "Burrito"

@route('/getMeat', method='GET')
def getMeat():
    print "I would Like to have Chicken"
    return "Chicken"

@route('/getRice', method='GET')
def getRice():
    print "I would Like to have Brown Rice"
    return "Brown"

@route('/getBeans', method='GET')
def getBeansi():
    print "I would Like to have Pinto Beans"
    return "Pinto"

@route('/getSauce', method='GET')
def getSauce():
    print "I would Like to have Corn,Mayo"
    return "Corn,Mayo"

@route('/getGarnish', method='GET')
def getSauce():
    print "I would Like to have Cheese"
    return "Cheese"

@route('/sendBill', method='POST')
def sendBill():
    bill=request._get_body_string()
    payBill(bill)
    print bill
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
        print "Bye"







if __name__ == '__main__':
    run(host='localhost',port =9080)
