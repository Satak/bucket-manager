from os import getenv
from google.cloud import storage
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_basicauth import BasicAuth

app = Flask(__name__)
storage_client = storage.Client()
BUCKET_NAME = getenv('BUCKET_NAME')
app.config['BASIC_AUTH_USERNAME'] = getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = getenv('BASIC_AUTH_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """Lists all the blobs in the bucket that begin with the prefix."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    return [blob for blob in blobs]


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file_name)
    #blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


@app.route('/')
def index():
    files = list_blobs_with_prefix(BUCKET_NAME, 'Videos')
    #for file in files:
    #    for key, value in file.__dict__.items():
    #            print(file.name, key, value)
    return render_template('index.html', files=files)


@app.route('/upload')
def upload_view():
    return render_template('upload_form.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    print(file.filename)
    upload_blob(BUCKET_NAME, file, f'Videos/{file.filename}')
    return redirect(url_for('index'))


@app.route('/files', methods=['DELETE'])
def delete_file():
    file = request.files['file']
    print(file.filename)
    upload_blob(BUCKET_NAME, file, f'Videos/{file.filename}')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
