"""Flask server."""

from flask import Flask, render_template, request, url_for, redirect
# from flask import send_from_directory
import os
import csv

app = Flask(__name__)  # use flask class to instantiate a flask app
print(__name__)  # name is __main__


# app.add_url_rule('/favicon.ico',
#            redirect_to=url_for('static', filename='./assets/favicon.ico'))


def valid_contact(data):
	"""Check contact form submitted by user."""
	for k, v in data.items():
		if not v:
			return False
	return True


@app.route('/')  # decorator - when you see slash, do this
def home():
	"""Define the route for the home page at 127.0.0.1:5000/."""
	return render_template('index.html', title='Welcome to Loverfinderzz!')


@app.route('/<string:page_name>')
def html_page(page_name):
	"""Define the route for all pages with a name e.g. index, about, contact.."""
	title = page_name.rpartition('.')[0].capitalize()
	return render_template(page_name, title='Loverfinderzz - ' + title)


def write_to_file(data):
	"""Write the user contact to database."""
	with open('database.txt', mode='a') as database:
		name = data['name']
		email = data['email']
		subject = data['subject']
		message = data['message']  # This needs to be encoded somehow!
		file = database.write(f'\n{name},{email},{subject},{message}')


def write_to_csv(data):
	"""Write the user contact to database as csv"""
	# Write header
	if not os.path.exists('database.csv'):
		with open('database.csv', mode='w') as database2:
			database2.write('name,email,subject,message\n')	
	# Write row
	with open('database.csv', mode='a', newline='') as database2:
		name = data['name']
		email = data['email']
		subject = data['subject']
		message = data['message']  # This needs to be encoded somehow!
		csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([name, email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	"""Load this template when user correctly submits an email form."""
	# error = None
	if request.method == 'POST':
		data = request.form.to_dict()
		if valid_contact(data):
			write_to_csv(data)
			# greet user by name
			return render_template('/submit_form.html', name=data['name'].split(' ')[0])
		else:
			error = 'ERROR: PLEASE COMPLETE ALL FIELDS IN THE CONTACT FORM!'
			return render_template('contact.html', error=error)
			# return 'something went wrong'
	#     if valid_login(request.form['username'],
	#                    request.form['password']):
	#         return log_the_user_in(request.form['username'])
	#     else:
	#         error = 'Invalid username/password'
	# # the code below is executed if the request method
	# # was GET or the credentials were invalid
	error = 'GET request method received when POST method was expected!'
	return render_template('submit_form.html', error=error)


# @app.route("/<username>/<int:post_id>")
# def hello_user(username=None, post_id=None):
# 	"""Display the user e.g. /brian on the index.html."""
# 	return render_template('index.html', name=username, post_id=post_id)


# @app.route('/person.ico')
# def favicon():
# 	"""Commment."""
# 	return send_from_directory(
# 		os.path.join(app.root_path, 'static'),
# 		'person.ico', mimetype='image/vnd.microsoft.icon')


# @app.route("/blog")
# def blog():
# 	"""Comment here."""
# 	return "<p>Blog blogs blogs are here.</p>"


# @app.route("/blog/2020/dogs")
# def blog_dog():
# 	"""Comment here."""
# 	return "<p>Dog blogs dog blogs are here.</p>"
