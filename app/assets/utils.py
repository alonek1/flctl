from app.assets.connection import Conn
site='127.0.0.1'
port='8080'

def timeconv(timeinsec):

    time=int(timeinsec['systemUptimeMsec'])
    x = time / 1000
    seconds = x % 60
    x /= 60
    minutes = x % 60
    x /= 60
    hours = x % 24
    x /= 24
    days = x
    return {'min':int(minutes),'hr':int(hours),'day':int(days)}


def get_switch_list():
    con=Conn(site,port)
    uri_static_pusher='/wm/core/controller/switches/json'
    switch_list = con.get(uri_static_pusher)
    return (switch_list)


