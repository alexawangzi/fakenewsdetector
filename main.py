# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import json

from flask import Flask, render_template

app = Flask(__name__)



@app.route('/', methods=['POST'])
def root():
    from flask import request
    req_json = request.get_json()
    annotation = annotate_text(req_json)
    keywords = filter_keywords(annotation)
    news = fetch_news(keywords)

    return news


def encode_url(keywords):
    encoded = 'q='
    for i in keywords:
        encoded = encoded + i + '%20'
    encoded = encoded + '&'

    return encoded


def fetch_news(keywords):
    import requests

    encoded = encode_url(keywords)
    url = ('https://gnews.io/api/v3/search?' +
           encoded +
           'token=1376d43c67cb5722c9837cdc4dc8617c')
    response = requests.get(url)

    return response.json()


def filter_keywords(annotation):
    keywords = [element['name'] for element in annotation['entities']]

    # TODO: further filter keywords

    print(keywords)

    return keywords


def annotate_text(req_json):
    print(req_json)

    from apiclient.discovery import build
    nlpapikey = 'AIzaSyDGz8ELBxqAGhBw5CWfDE1YxGigbrkf6QU'

    service = build('language', 'v1', developerKey=nlpapikey)
    collection = service.documents()

    data = {}
    data['document'] = {}
    data['document']['language'] = 'en'
    data['document']['content'] = req_json['newsContent']
    data['document']['type'] = 'PLAIN_TEXT'

    data['features'] = {}
    # data['features']['extractSyntax'] = True
    data['features']['extractEntities'] = True
    # data['features']['extractDocumentSentiment'] = True
    # data['features']['extractEntitySentiment'] = True

    requestToAPI = collection.annotateText(body=data)
    annotation = requestToAPI.execute()

    print(json.dumps(annotation, indent=2, sort_keys=True))

    return annotation



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
