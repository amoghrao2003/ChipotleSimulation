

from bottle import request,route,static_file,run
import BaseWorker as workers



@route('/markPresence', method='POST')
def markPresence():
    requestBody = request._get_body_string()
    workers.orderQueue.put(requestBody)


    print requestBody
    return "Success"



if __name__ == '__main__':
    workers.startWorker()
    run(host='localhost',port =8080)


