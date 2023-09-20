from flask import Flask, jsonify, redirect, url_for, request, render_template
import os, inference_web

UPLOAD_FOLDER = 'static/results/'

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    return jsonify({'result': 'this supports api only'})

@app.route('/wav2lip/<audioFile>/<imgFile>/<outputFile>')
def wav2lip(audioFile, imgFile, outputFile):
	print('audioFile: ' + audioFile)
	print('imgFile: ' + imgFile)
	print('outputFile: ' + outputFile)
	audioFilepath = os.path.join(app.instance_path, audioFile)
	imgFilepath = os.path.join(app.instance_path, imgFile)
	outputFilepath = UPLOAD_FOLDER + outputFile
	inference_web.makeFace(audioFilepath, imgFilepath, outputFilepath)
	return jsonify({'result': 'success'})

if __name__ == '__main__':
	app.run(debug=True)
