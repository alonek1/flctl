from flask_wtf import Form
from wtforms import StringField, BooleanField,PasswordField,SelectField
from wtforms.validators import DataRequired
from .assets import utils
class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()],render_kw={"placeholder": "username"})
    password = PasswordField('password', validators=[DataRequired()],render_kw={"placeholder": "password"})
    #remember_me = BooleanField('remember_me', default=False)

class StaticPushForm(Form):

    switch_list=utils.get_switch_list()

    #switch_choice(switch_list)
    if switch_list is not None:
        try:
            switches_auto = SelectField(u'switch')
            for switch in switch_list:
                 switches_auto.choices = switch
        except:
             switches_auto = SelectField(u'switch',choices=[('No Switch is avalaible', 'No Switch is avalaible')])
    else:
        switches_auto = SelectField(u'switch',choices=[('No Switch is avalaible', 'No Switch is avalaible')])

    name = StringField('name', validators=[DataRequired()],render_kw={"placeholder": "name"})
    #set cookie by urself
    priority = StringField('priority', validators=[DataRequired()],render_kw={"placeholder": "priority"})
    inport = StringField('in_port', validators=[DataRequired()],render_kw={"placeholder": "in port"})
    ethertype = StringField('ethertype', validators=[DataRequired()],render_kw={"placeholder": "ether type"})
    active = SelectField('active', choices=[('true', 'true'), ('false', 'false')])
#for automaticly load switches mac as selectbox
#def switch_choice (switch_list):












