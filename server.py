from flask import Flask, redirect, request
from flask import render_template, url_for
import os
import time
import subprocess
from werkzeug.utils import secure_filename
import shutil


app = Flask("Simple-Web-Server")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = 'images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
	app.logger.error('Page not found: %s', (request.path))
	return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return redirect(url_for("classification"), code=302)


@app.route('/wait')
def wait():
    time.sleep(2)
    return ''

@app.route('/classification', methods=['GET'])
def classification():
    return render_template('classification.html')


        
@app.route('/mnist', methods=['GET', 'POST'])
def mnist():
    if request.method == 'GET':
        return render_template('mnist.html')

    elif request.method == 'POST':
        # if file not send
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("mnist"), code=302)
        
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


@app.route('/imagenet', methods=['GET', 'POST'])
def imagenet():
    if request.method == 'GET':
        return render_template('imagenet.html')

    elif request.method == 'POST':
        # if file not send
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("mnist"), code=302)
        
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            process = subprocess.Popen('python3 models/ImageNet/classify_image.py \
                                        --image_file {}'.format(path),\
                                                        shell=True, \
                                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE)
                                                                 
            prediction = process.stdout.read().decode("utf-8") 
            prediction.replace(")", ")<br></br>")
            err = process.stderr.read()

            new_path = 'static/{}'.format(filename)
            shutil.copy(path, new_path)
            return '<h1>Classification result: <br></br>\
            {}<h1> <br></br> <img src="{}">'.format(prediction, new_path)





if __name__ == '__main__':

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
