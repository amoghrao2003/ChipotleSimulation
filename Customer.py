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

if __name__ == '__main__':
    run(host='localhost',port =9080)
