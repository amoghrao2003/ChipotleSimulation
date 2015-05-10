__author__ = 'voldy'


#Pai
from bottle import request,route,static_file,run

@route('/getBase', method='GET')
def getBase():
    print "I would Like to have Burrito"
    return "Burrito"

@route('/getMeat', method='GET')
def getMeat():
    print "I would Like to have Chicken"
    return "Chicken"


@route('/sendBill', method='POST')
def sendBill():
    bill=request._get_body_string()
    print bill
    return "bill received"

if __name__ == '__main__':
    run(host='localhost',port =9080)
