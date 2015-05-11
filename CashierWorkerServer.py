__author__ = 'Abhinav'


from bottle import request,route,static_file,run
import CashierWorker as workers


@route('/send', method='POST')
def send():
    workers.billQueue.put(request._get_body_string())
    #print requestBody
    return "Success"

@route('/payBill', method='POST')
def payBill():
    return "Have a great Day !!!"



if __name__ == '__main__':
    workers.startWorker()
    run(host='localhost',port =8084)
