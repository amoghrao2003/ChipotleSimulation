__author__ = 'Abhinav'


from bottle import request,route,static_file,run
import CashierWorker as workers


@route('/sendMeat', method='POST')
def sendMeat():
    workers.billQueue.put(request._get_body_string())
    #print requestBody
    return "Success"

if __name__ == '__main__':
    workers.startWorker()
    run(host='localhost',port =8085)
