#todo change views to not need for handling
#hieraachy kardane template ha
import os
import json
from flask import render_template, flash, redirect, session, url_for, request, g
from app import app
from app import app, db, login_manager
from flask_login  import login_user, logout_user, current_user, login_required
from .forms import LoginForm,StaticPushForm
from .models import User
from flask import send_from_directory
from app.assets.connection import Conn
from app.assets.utils import timeconv,get_switch_list



site='127.0.0.1'
port='8080'
#@login_manager.user_loader
#def load_user(id):
#    return USERS.get(int(id))
@app.route('/',methods=('GET', 'POST'))
def login():
    #g global is setup by Flask as a place to store and share data during the life of a request. // it's global and usable in everwhere (even in templates)
    #check if user is authenticated redirect ir directly to panel
    g.user = current_user
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('panel'))
    form = LoginForm()

    #If everything is ok with the form submitation
    if form.validate_on_submit():
        #return redirect('/panel')#we also can use some flash here to send  datat (like username) to present on next page (via get_flashed_messages() )
        #session['username']= form.username.data #Once data is stored in the session object it will be available during that request and any future requests made by the same client
        #session['password']= form.password.raw_data

        #Flask-login will try and load a user BEFORE every request
        #it is used to check what userid is in the current session and will load the user object for that id
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            _user = User.query.filter_by(username=username,password=password).first()
            #if user wasn't authenticated
            if _user is None:
                flash('Username or Password is invalid' , 'error')
                return redirect('/')
                #add flash here
            else:
                login_user(_user)


        #user = User(username=session['username'], password=session['password'])
        #login_user(user)
        #g.user = current_user
        return redirect(request.args.get('next') or url_for('panel'))
    return render_template('login.html',
                           form=form)



@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/panel/')
@login_required
def panel():
    uri_uptime='/wm/core/system/uptime/json'
    uri_memoryload = '/wm/core/memory/json'
    uri_loadedmodule = '/wm/core/module/loaded/json'
    uri_static_pusher='/wm/core/controller/switches/json'
    con=Conn(site,port)
    res=con.get(uri_uptime)
    uptime=timeconv(res)
    memoryload=con.get(uri_memoryload)
    loadedmodules=con.get(uri_loadedmodule)
    switch_list = con.get(uri_static_pusher)

    return render_template('panel.html',uptime=uptime,memoryload=memoryload,loadedmodules=loadedmodules,type=switch_list)#,url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity=url_portsecurity,url_stp=url_stp)

@app.route('/panel/routing',methods=('GET', 'POST'))
@login_required
def routing():
    form=StaticPushForm()
    # uri_static_pusher='/wm/core/controller/switches/json'
    # con=Conn(site,port)
    # switch_list = con.get(uri_static_pusher)
    # str1 = ''.join(switch_list[0])
    # json_list=json.loads(str1)
    # j=json_list['switchDPID']
    if request.method == 'POST':
        switch = request.form['switch']
        name = request.form['name']
        priority = request.form['priority']
        in_port = request.form['in_port']
        active=request.form['active']
        eth_des = request.form['eth_des']
        eth_type = request.form['eth_type']
        action = request.form['action']
        cookie = '0'
        if  eth_type != '' and  in_port == '':
            data = {
                'switch':"{}".format(switch),
                "name" : "{}".format(name),
                "cookie":"0",
                "priority":"{}".format(priority),
                "eth_type":"{}".format(eth_type),
                "active":"{}".format(active),
                "actions" :"{}".format(action)
            }
        elif eth_type !='' and in_port !='' :

            data = {
                'switch':"{}".format(switch),
                "name" : "{}".format(name),
                "cookie":"0",
                "priority":"{}".format(priority),
                "in_port":"{}".format(in_port),
                "active":"{}".format(active),
                "eth_type":"{}".format(eth_type),
                "actions" :"{}".format(action)
            }

        else:
            data = {
                'switch':"{}".format(switch),
                "name" : "{}".format(name),
                "cookie":"0",
                "priority":"{}".format(priority),
                "eth_dst":"{}".format(eth_type),
                "active":"{}".format(active),
                "actions" :"{}".format(action)
            }
        uri_static_pusher_post = '/wm/staticflowpusher/json'
        con=Conn(site,port)
        con.post(uri_static_pusher_post,data)

    return render_template('routing.html',form=form)#, url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity=url_portsecurity,url_stp=url_stp)

@app.route('/panel/stp')
@login_required
def stp():
    return render_template('stp.html')#,url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity=url_portsecurity,url_stp=url_stp,url_panel=url_panel)

@app.route('/panel/etherchannel')
@login_required
def etherchannel():
    return render_template('etherchannel.html')#,url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity=url_portsecurity,url_stp=url_stp,url_panel=url_panel)


@app.route('/panel/settings')
@login_required
def settings():
    return render_template ('settings.html') #,url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity#=url_portsecurity,#url_stp=url_stp,url_panel=url_panel)

@app.route('/panel/dai')
@login_required
def dai():
    return render_template('dynamicarp.html',user=current_user)#,url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity=url_portsecurity,url_stp=#url_stp,url_panel=url_panel)

@app.route('/panel/portsecurity')
@login_required
def portsecurity():
    return render_template('portsecurity.html')#,url_dynamicarp=url_dynamicarp,url_etherchannel=url_etherchannel,url_route=url_route,
                           #url_portsecurity=url_portsecurity,url_stp=#url_stp,url_panel=url_panel)


@app.route('/fonts/<path:filename>')
def serve_static2(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'fonts'), filename)

#load and sending static files
#will change such thing static/fontawesome-webfont.eot to this /static/css/static/fontawesome-webfont.woff
@app.route('/static/<path:filename>')
def serve_static(filename):

    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'css'), filename)
