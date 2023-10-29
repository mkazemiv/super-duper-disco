from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os, requests
from requests import get
from supabase import create_client, Client #, ClientOptions
import traceback
import logging
import json

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
# options = ClientOptions()
# options.headers = {"persistSession": False}
supabase: Client = create_client(url, key)
# supabase.storage.from_('gfgg')
site_url = 'http://localhost:5000'
currEmail = ''
UPLOAD_FOLDER = 'static/results/'

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.gif', '.aac', '.mp3', '.m4a', '.ogg', '.wav', '.wma']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def index():
    return render_template('subscription.html')

@app.route('/subscribe_diamond')
def subscribe_diamond():
	return redirect('https://3046.chickenkiller.com:8443/diamond', code=301)

@app.route('/subscribe_rocket')
def subscribe_rocket():
	return redirect('https://3046.chickenkiller.com:8443/rocket', code=301)

@app.route('/success/<name>')
def success(name, audiofile):
	return 'welcome %s %s %s' % name, audiofile #, file

@app.route('/confirm', methods = ['POST'])
def confirm():
	if request.method == 'POST':
		email = request.form['email']
		data_id = request.form['data_id']

		data, count = (supabase
		.table('wailist') 
		.insert({
			"user_id": data_id,
			"email": email})
		.execute())
	return render_template('confirmation.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		try:
			data_id = request.form['data_id']
			print("(/uploader) data_id received:", data_id)
			audioFile = request.files['audioFile']
			audioFilename = secure_filename(audioFile.filename) # save file 
			if audioFilename != '':
				file_ext = os.path.splitext(audioFilename)[1]
				if file_ext.lower() not in app.config["UPLOAD_EXTENSIONS"][3:]:
					flash("Invalid file extension; audio file name should end with one of the following: " 
		   					+ str(app.config["UPLOAD_EXTENSIONS"][3:]))
					return render_template('upload.html', data_id=request.form['data_id'])
				audioFilepath = os.path.join(UPLOAD_FOLDER, audioFilename)
				audioFile.save(audioFilepath)

			imgFile = request.files['imgFile']
			imgFilename = secure_filename(imgFile.filename) # save file 
			if imgFilename != '':
				file_ext = os.path.splitext(imgFilename)[1]
				if file_ext.lower() not in app.config["UPLOAD_EXTENSIONS"][:3]:
					flash("Invalid file extension; image file name should end with one of the following: " 
		   					+ str(app.config["UPLOAD_EXTENSIONS"][:3]))
					return render_template('upload.html', data_id=request.form['data_id'])
				imgFilepath = os.path.join(UPLOAD_FOLDER, imgFilename)
				imgFile.save(imgFilepath)

			outputFilename = f"merge-{data_id}.mp4"
			outputFilepath = UPLOAD_FOLDER + outputFilename

			data, count = (supabase
			.table('files')
			.insert({
				"output_file": outputFilepath,
				"user_id": data_id,
				"audio_file": audioFilepath,
				"image_file": imgFilepath
				})
			.execute())
		except Exception as e:
			logging.error(traceback.format_exc())

		return render_template('download.html', data_id=data_id)
	else:
		print('args', request.args)
		print('files', request.files)

# was /register
@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		data_id = request.form['data_id']
		return render_template('upload.html', data_id=data_id)
	else:
		# TODO render 400 instead of upload.html
	    return render_template('upload.html')

# @app.route('/login', methods=['POST', 'GET'])
# def login():
# 	if request.method == 'POST':
# 		print(request.form)
# 		user = request.form['nm']
# 		audiofile = request.files['audiofile']
# 		return redirect(url_for('success', name=user, audiofile=audiofile))
# 	else:
# 		user = request.args.get('nm')
# 		return redirect(url_for('success', name=user))

@app.route('/sign-up')
def signup():
	return render_template('sign-up.html')

@app.route('/trial', methods=['POST'])
def free_trial():
	# query DB to check if user already exists
	queryRes = query_by_email(request.form['email'])
	print("/trial, fetch response:", queryRes)
	
	# if user does exist...
	if queryRes != None:
		global currEmail; currEmail = queryRes['email']
		print("/trial: user already exists, redirecting to /home...")
		return redirect(url_for('home'))

	return render_template('register.html', email=request.form['email'], password=request.form['password'])

# serves as a buffer that allows user to verify email and then get into acct via emailed verification link
@app.route('/verify', methods=['POST', 'GET'])
def verify():
	print('/verify, request data:', request.form)
	# if request.method != 'POST':
		# TODO: make static/ files for 400
		# endpoint should only be reachable after sign-up
	if request.method == 'POST':
		res = supabase.auth.sign_up({
			"email": request.form['email'],
			"password": request.form['password']
		})
		print("sign_up() AuthResponse:", res)

		post_dict = request.form.to_dict()
		# delete password since we passed it secretly, but don't want to insert it into db 
		del post_dict['password']

		print("inserting new user data into db (post_dict):", post_dict)
		data, count = supabase.table('users').insert(post_dict).execute()
		print("insertion return data:", data)

		return render_template('verify.html', email=request.form['email'], password=request.form['password'])
	else:
		return render_template('verify2.html')

@app.route('/sign-in')
def signin():
	if currEmail != '':
		# bypassing sign-in page if user is already logged in
		return redirect(url_for('home'))
	return render_template('sign-in.html')

# use /verify-email as field for user to enter OTP code
# whether post or get, have links to sign in/up pages and 

@app.route('/home', methods=['POST', 'GET'])
def home():
	global currEmail
	queryRes = None
	# print(type(request.form))
	if request.method == 'POST':
		queryRes = query_by_email(request.form['email'])
		# if user attempting to sign in exists...
		if queryRes != None:
			# user signing in is verified, so sign-in & update `currEmail`
			if queryRes['verified'] == True:
				try:
					supabase.auth.sign_in_with_password({
						"email": request.form['email'],
						"password": request.form['password']
					})
					currEmail = request.form['email']
					print("signed in as user", currEmail)
				except Exception as ex:
					# most likely AuthApiError
					print("Sign-in exception caught:", type(ex).__name__)
					# TODO is this the only possibility?
					flash("Login error: incorrect password")
					return redirect(url_for('signin'))
			# user isn't verified but a(n) OTP is supplied (first-time sign-in)
			elif queryRes['verified'] == False and request.form['otp']:
				try:
					verifyRes = supabase.auth.verify_otp({
						'email': request.form['email'], 
						'token': request.form['otp'], 
						'type': 'signup'
					})
					print('/home, verifyOTP result:', verifyRes)

					# update verification status
					supabase.auth.sign_in_with_password({
						"email": request.form['email'],
						"password": request.form['password']
					})

					# set global `currEmail` to the given email
					currEmail = request.form['email']
					
					# update user's verification status
					data, count = (supabase
						.table('users')
						.update({'verified': True})
						.eq('email', request.form['email'])
						.execute()
					)
					print('update reponse:', data)
				except Exception as ex:
					print("exception caught:", type(ex).__name__)
					# flash("exception caught:", type(ex).__name__)
					# return redirect(url_for('signin'))
		else:
			print("user siging in DNE, redirecting to /sign-in...")
			return redirect(url_for('signin'))
	
	# check if there is not an active user
	if currEmail == '':
		print('/home: no logged in user, redirecting to /sign-in')
		return redirect(url_for('signin'))
	if queryRes == None:
		queryRes = query_by_email(currEmail)
	# print("/home, fetch response:", query.data)

	if queryRes != None:
		return render_template('home.html', data_id = queryRes['id'], name = queryRes['full_name'])
	else:
		print("user DNE in db")
		return redirect(url_for('free_trial'))

@app.route('/sign-out')
def signout():
	global currEmail
	print("signing out from", currEmail)
	supabase.auth.sign_out()
	currEmail = ''
	return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def pw_reset_req():
	if request.method == 'GET':
		# user entering email for password reset
		return render_template('forgot-password.html')
	else:
		# processing pw reset email
		# TODO: handle 'gotrue.errors.AuthApiError: For security purposes, you can only request this once every 60 seconds'
		supabase.auth.reset_password_email(
						email = request.form['email'],
						options = {'redirect_to': site_url+'/update-password'}
					)
		return render_template('reset-email-sent.html')

@app.route('/update-password', methods=['GET', 'POST'])
def reset_password():
	if request.method == 'GET':
		return render_template('verify2.html')
	else:
		global currEmail
		print('form data:', request.form)
		siwotp = supabase.auth.verify_otp({
						'email': request.form['email'],
						'token': request.form['otp'],
						'type': 'recovery'
					})
		print('sign in result:', siwotp)
		try:
			currUser = supabase.auth.get_user()
			print('get_user():', currUser)
			currEmail = request.form['email']
		except Exception as ex:
			print('get_user() exception:', ex)

		try:
			supabase.auth.update_user({'password': request.form['new_password']})
			queryRes = query_by_email(currEmail)
			if queryRes != None:
				return redirect(url_for('home'))
			else:
				print("user DNE in db")
				currEmail = ''
				return redirect(url_for('free_trial'))
		except Exception as ex:
			print("Password update exception caught:", type(ex).__name__)
			flash("Password update exception caught:", type(ex).__name__)
			# TODO 500 Exception caught
			return render_template('500.html')

def query_by_email(email_to_fetch):
	
	print("querying public.users table for", email_to_fetch, '...')
	query = supabase.table('users').select("*").eq('email', email_to_fetch).execute()

	if query.data != []:
		response = query.json(exclude_none=True)
		# print("response:", response)
		data_list = json.loads(response)
		print("returning query result:", data_list['data'][0])
		return data_list['data'][0]
	else:
		print("retruned None, no such user found in db")
		flash("No user found. Are you using the right credentials?")
		return None

if __name__ == '__main__':
	app.run(debug=True)
