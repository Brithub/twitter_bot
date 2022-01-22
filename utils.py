from google.cloud import storage
from nltk import word_tokenize, pos_tag
from nltk import Tree
from nltk import RegexpParser
import nltk
from google_images_search import GoogleImagesSearch
import os
import re


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    return blobs


def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))


def get_blob(bucket_name, key, destination):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(key)
    blob.download_to_filename(destination)


def get_bad_phrases(bucket, key):
    get_blob(bucket, key, "/tmp/temp_bad_words.txt")
    f = open("/tmp/temp_bad_words.txt", "r")
    content = f.read()
    f.close()
    return content.split("\n")


def get_subject(phrase):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
    chunker = RegexpParser(NP)
    parse = chunker.parse
    chunked = parse(pos_tag(word_tokenize(phrase)))
    continuous_chunk = []
    current_chunk = []
    backup = []

    for subtree in chunked:
        if type(subtree) == tuple and subtree[1] == "NN":
            backup.append(subtree[0])
        if type(subtree) == Tree:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    if len(continuous_chunk) is 0:
        return backup

    return continuous_chunk


def download_image(query):

    consumer_key = os.environ['SEARCH_KEY']
    consumer_secret = os.environ['SEARCH_CX']

    gis = GoogleImagesSearch(consumer_key, consumer_secret)

    # define search params:

    _search_params = {
        'q': query,
        'num': 1,
        'fileType': 'jpg',
        'safe': 'medium'
    }

    # this will search, download and resize:
    gis.search(search_params=_search_params, path_to_dir="/tmp/", custom_image_name=query)


def clean_text(edited):
    """
    This is the main text cleanup done in the project.
    Tweets are in english, and have all kinds of @s, hashtags, and general nonsenses
    This function basically tries to clean that up
    """
    edited = re.sub("^(RT|rt) .*", "", edited)
    edited = re.sub("^@.*", "", edited)
    edited = re.sub("@", "", edited)
    edited = re.sub("“", "\"", edited)
    edited = re.sub("”", "\"", edited)
    edited = re.sub(r"^(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub(r"^\"(@\w?[^\s]+)(.@\w?[^\s]+)*", "", edited)
    edited = re.sub("\n", " ", edited)
    edited = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", edited)
    edited = re.sub("-", " ", edited)
    edited = re.sub("\\\\", " ", edited)
    edited = re.sub("/", " ", edited)
    edited = re.sub("^ ", "", edited)
    edited = re.sub(r"^ +", "", edited)
    edited = re.sub(r" $", "", edited)
    edited = re.sub("/", " ", edited)
    edited = re.sub(" {2}", " ", edited)
    edited = re.sub("^ ", "", edited)
    edited = re.sub(r"^ +", "", edited)
    edited = re.sub(r" $", "", edited)

    return edited
