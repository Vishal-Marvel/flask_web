from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, BooleanField
from wtforms.validators import DataRequired
import pickle

class LoginForm(FlaskForm):
	u_name = StringField("Username", validators=[DataRequired()])
	pass_w = PasswordField("Password", validators=[DataRequired()])
	check = BooleanField('Show password', id='check')
	submit = SubmitField("Submit")

class CreateUserForm(FlaskForm):
	name = StringField("Username", validators=[DataRequired()])
	f_name = StringField("First name", validators=[DataRequired()])
	l_name = StringField("Last name", validators=[DataRequired()])
	security_q = StringField("Whats your school name (for resetting password incase if you forget it)", validators=[DataRequired()])
	pass_w = PasswordField("Password", validators=[DataRequired()],id='pass_w')
	check = BooleanField('Show password', id='check')
	submit = SubmitField("Submit")

class ResetPasswordForm(FlaskForm):
	name = StringField("Username", validators=[DataRequired()])
	answer = StringField("Whats your school name:", validators=[DataRequired()])
	o_pass_w = PasswordField("Old Password", validators=[DataRequired()],id='o_pass_w')
	n_pass_w = PasswordField("New Password", validators=[DataRequired()],id='n_pass_w')
	check = BooleanField('Show password', id='check')
	submit = SubmitField("Submit")

def write_data(dic):
	data = dict()
	try:
		file = open('data.dat', 'rb')
		data = pickle.load(file)
	except EOFError:
		pass
	except FileNotFoundError:
		pass
	data = dic
	file = open('data.dat', 'wb')
	pickle.dump(data, file)

def get_data():
	data = dict()
	try:
		file = open('data.dat', 'rb')
		data = pickle.load(file)
	except EOFError:
		pass
	except FileNotFoundError:
		pass
	return data