__author__ = 'pai'
import bottle,pymysql, jaraco.itertools
import json
from bottle import response, request


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()
#mydata = '{ "result": [ { "customer_name": "Nikhil-Paniker", "progress": 3 }, { "customer_name": "Ameya-K", "progress": 10 }, { "customer_name": "amogh", "progress": 2 }, { "customer_name": "Dada", "progress": 6 } ] }'
#mydata ='[["John", 5], ["Amogh", 1], ["NIkhil", 4], ["Khadilkar", 3], ["Kadam", 3], ["Montu", 2], ["Panicker", 1], ["Nikhil2", 5], ["Nikhil1", 5], ["Codilkar", 5], ["Codilkar", 5], ["Codilkar", 5], ["Codilkar", 5], ["Codilkar", 5], ["Ameya", 5], ["Ameya", 5]]'
mydata = ''

@app.route('/cors', method=['OPTIONS', 'GET'])
def lvambience():
    response.headers['Content-type'] = 'application/json'
    return mydata
    #lvambience

@app.route('/getMyData', method=['OPTIONS','GET'])
def myGraph():
    response.headers['Content-type'] = 'application/json'
    conn = pymysql.connect(host='dbinstance-sjsu-amogh.cyht8ykut6xk.us-west-1.rds.amazonaws.com', port=3306, user='voldy', passwd='voldysjsu', db='cmpe275')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Orders")
    rows = cur.fetchall()
    desc = cur.description
    print(desc);
    rowarray_list = []
    for row in rows:
        #print(row[0])
        t = (row[0], row[1])
        rowarray_list.append(t)
    j = json.dumps(rowarray_list)
    print(j)
    return j


app.install(EnableCors())

app.run(port=8006)
