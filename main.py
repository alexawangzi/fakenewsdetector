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


@app.route('/')
def root():
    from apiclient.discovery import build

    apikey = 'AIzaSyDGz8ELBxqAGhBw5CWfDE1YxGigbrkf6QU'

    service = build('language', 'v1', developerKey=apikey)
    collection = service.documents()

    data = {}
    data['document'] = {}
    data['document']['language'] = 'en'
    data['document']['content'] = 'I am really happy'
    data['document']['type'] = 'PLAIN_TEXT'

    request = collection.analyzeSentiment(body=data)
    sentiment = request.execute()

    return json.dumps(sentiment)

    #
    # return json.dumps('Sentiment: {}, {}'.format(sentiment.documentSentiment.score, sentiment.documentSentiment.magnitude))


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
