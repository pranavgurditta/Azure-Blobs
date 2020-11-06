import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from azure.storage.blob import BlockBlobService
import string, random, requests

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')
account = 'storageaiproject'  # Azure account name
key = 'qyMSPkxdMYp8ESp9aIds7RFCJnTcOQZK9pw84+1GScvr/8DGtE1Ak5Nl1gL33sAecXMmS3B9M2kAiblr9BeHvA'     # Azure Storage account access key  
container = 'ok'# Container name

blob_service = BlockBlobService(account_name=account, account_key=key)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    	file = request.files['file']
    	filename = secure_filename(file.filename)
    	fileextension = filename.rsplit('.',1)[1]
        Randomfilename ='image'
        filename = Randomfilename + '.' + fileextension
        try:
            blob_service.create_blob_from_stream(container, filename, file)
        except Exception:
            print 'Exception=' + Exception 
            pass
        ref =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
        return '''
	    <!doctype html>
	    <title>File Link</title>
	    <h1>Uploaded File Link</h1>
	    <p>''' + ref + '''</p>
	    <img src="'''+ ref +'''">
	    '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    app.run(debug=True)
