__author__ = 'voldy'

from bottle import request,route,static_file,run
import SauceWorker as workers

@route('/send', method='POST')
def send():
    workers.sauceQueue.put(request._get_body_string())
    #print requestBody
    return "Success"



if __name__ == '__main__':
    workers.startWorker()
    run(host='localhost',port =8082)