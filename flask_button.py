import os
from io import BytesIO
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, flash, request, redirect, url_for, send_from_directory, send_file, render_template
from werkzeug.utils import secure_filename
import numpy as np

UPLOAD_FOLDER = '/home/snowowl/anaconda3/envs/openmlcourse/openml_tasks/CFT_flask_task/uploads'
STATIC_FOLDER = '/home/snowowl/anaconda3/envs/openmlcourse/openml_tasks/CFT_flask_task/static'
ALLOWED_EXTENSIONS = {'mp3', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER


def allowed_file(filename):
    '''
    Check extension if it in in ALLOWED_EXTENSIONS or not
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    '''
    Upload file to UPLOAD_FOLDER and redirect to fig()
    '''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('fig',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    '''
    Upload file to UPLOAD_FOLDER and return file to user(NOT USED)
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/fig/<filename>')
def fig(filename):
    '''
    Load music file to librosa and create spectrogram with librosa.stft()
    Returns: html template with .png image of spectrogram
    '''
    data_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    y, sr = librosa.load(data_file)
    print(y)
    D = librosa.stft(y)
    plt.title('Power spectrogram')
    plt.tight_layout()
    fig = plt.Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    p = librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), ax=ax, y_axis='log', x_axis='time')
    fig.savefig(os.path.join(app.config['STATIC_FOLDER'], 'spec.png'))
    return render_template('spektr.html')
  
