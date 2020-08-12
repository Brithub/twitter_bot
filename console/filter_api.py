import logging
from google.cloud import storage
import os


def update_filter(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': ['POST', 'GET'],
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return '', 204, headers

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    temp_path = "/tmp/badwords.txt"
    bucket_name = os.environ['BUCKET']
    key = "badwords.txt"
    request_json = request.get_json()

    if request.method == 'GET':
        get_blob(bucket_name, key, temp_path)
        f = open(temp_path, "r")
        content = f.read()
        f.close()
        return content, 200, headers

    if request.method == 'POST' and request_json and 'message' in request_json:
        message = request_json.get('message')
        if len(message) > 100 or len(message) < 5:
            return "Phrase needs to be between 5 and 100 characters!", 400, headers

        logging.info("adding " + request_json.get('message'))

        get_blob(bucket_name, key, temp_path)
        modify_filter(temp_path, request_json.get('message'))
        upload_blob(bucket_name, temp_path, key)
        return str(request_json.get('message')), 200, headers
    else:
        return str(request), 400, headers


def modify_filter(file, text):
    f = open(file, "a+")
    f.write("\n" + text)
    f.close()


def upload_blob(bucket_name, key, destination):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination)

    blob.upload_from_filename(key)


def get_blob(bucket_name, key, destination):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(key)
    blob.download_to_filename(destination)
