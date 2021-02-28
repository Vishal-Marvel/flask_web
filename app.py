from flask import Flask, render_template, flash, Markup, redirect, url_for
from forms import LoginForm, CreateUserForm, ResetPasswordForm
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

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


@app.route('/', methods=['GET', 'POST'])

def home():

	form = LoginForm()
	# Validate Form
	if form.validate_on_submit():
		data = get_data()
		
		for i in data.keys():
			if form.u_name.data == i:
				data = data[i]
				if form.pass_w.data == data['pass_w']:
					return redirect(url_for('page_1'))
				else:
					flash("Incorrect Password!")
					break
		else:
			flash(Markup('No Such user exists, Click <a href="/create_user" class="alert-link">here</a> to create one'))
	return render_template("login.html",
		form = form)

@app.route('/create_user', methods=['GET', 'POST'])

def create_user():
	name = None
	form = CreateUserForm()
	if form.validate_on_submit():
		data = get_data()
		for i in data.keys():
			if i == form.name.data:
				flash("User Name already exists")
				break
		else:
			user_dict = {
			'name': form.name.data, 
			'f_name': form.f_name.data,
			'l_name': form.l_name.data,
			'security_q': form.security_q.data,
			'pass_w': form.pass_w.data}
			data[user_dict['name']] = user_dict
			write_data(data)
			return redirect(url_for('home'))
	return render_template('create_user.html',
	form = form)

@app.route('/page_1')

def page_1():
	return render_template('page_1.html')

@app.route('/users')

def users():
	return render_template('users.html', users = get_data().keys())

@app.route('/user_profile/<name>')

def profile(name):
	data = get_data()[name]
	
	return render_template('profile.html', data=data)

@app.route('/reset_pass/<name>', methods=['GET', 'POST'])

def reset_pass(name):
	form = ResetPasswordForm()
	if form.is_submitted():
		
		data = get_data()[name]
		if data['pass_w'] == form.o_pass_w.data:
			
			data = get_data()
			u_data = data[name]
			del data[name]
			u_data['pass_w'] = form.n_pass_w.data
			data[u_data['name']] = u_data
			write_data(data)
			return redirect(url_for('home'))
			
		else:
			flash(Markup('Old Password Incorrect'))

	return render_template('reset_password.html', form=form, func='reset')

@app.route('/forgot_pass', methods=['GET', 'POST'])

def forgot_pass():
	form = ResetPasswordForm()
	if form.is_submitted():
		for i in get_data().keys():
			if form.name.data == i:
				data = get_data()[i]
				if data['security_q'] == form.answer.data:
					data = get_data()
					u_data = data[i]
					del data[i]
					u_data['pass_w'] = form.n_pass_w.data
					data[u_data['name']] = u_data
					write_data(data)
					return redirect(url_for('home'))
					break
				else:
					flash('Incorrect Answer')
					break
			else:
				flash('No such user exists')
				break

	return render_template('reset_password.html', form=form, func='forgot')

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500

	
if __name__ == '__main__':
	app.run(host='0.0.0.0')