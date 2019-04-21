from os import getenv
from google.cloud import storage
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_basicauth import BasicAuth
import logging

app = Flask(__name__)
storage_client = storage.Client()
BUCKET_NAME = getenv('BUCKET_NAME')
app.config['BASIC_AUTH_USERNAME'] = getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = getenv('BASIC_AUTH_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


def get_properties(files):
    for file in files:
        for key, value in file.__dict__.items():
            print(file.name, key, value)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    logging.info(f'Blob {blob_name} deleted.')


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None, file_type=''):
    """Lists all the blobs in the bucket that begin with the prefix."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    if file_type:
        return [blob for blob in blobs if blob.name[-len(file_type):] == file_type]
    return [blob for blob in blobs]


def upload_blob(bucket_name, source_file, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file)
    logging.info(f'File uploaded to {destination_blob_name}.')


@app.route('/')
def index():
    files = list_blobs_with_prefix(BUCKET_NAME, 'Videos')
    return render_template('index.html', files=files)


@app.route('/api/videos')
def api_get_videos():
    files = list_blobs_with_prefix(BUCKET_NAME, 'Videos', file_type='.mp4')
    videos = [file.name for file in files]
    return jsonify(videos)


@app.route('/videos')
def videos_view():
    videos = list_blobs_with_prefix(BUCKET_NAME, 'Videos', file_type='.mp4')
    return render_template('videos.html', videos=videos)


@app.route('/upload')
def upload_view():
    return render_template('upload_form.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    upload_blob(BUCKET_NAME, file, f'Videos/{file.filename}')
    return redirect(url_for('index'))


@app.route('/api/files/<string:file_name>', methods=['DELETE'])
def api_delete_file(file_name):
    delete_blob(BUCKET_NAME, file_name)
    return jsonify({}), 204


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
