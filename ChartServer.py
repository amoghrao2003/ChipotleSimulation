__author__ = 'pai'

from bottle import request,route,static_file,run, response

mydata = "{'result':[{'customer_name': 'amogh','progress': 3},{customer_name': 'nigga','progress': 9},{'customer_name': 'halkat_khadilkar','progress': 2},{'customer_name': 'dada','progress': 6}]}"


@route('/getGraphData', method='GET')
def getGraphData():
    print('hi')
    #return 'hi'
    return mydata;

if __name__ == '__main__':
    run(host='10.189.31.34',port = 8888)