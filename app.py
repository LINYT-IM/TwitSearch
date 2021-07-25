# import time
from TwitterAPI import TwitterAPI
import os
import json
import sys
from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment


app = Flask(__name__, static_url_path='', static_folder='./templates')
CORS(app)
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return render_template('index.html')

@app.route('/flask/search', methods = ['POST'])
def search():
    keys = {}
    keys['consumer_key'] = ''
    keys['consumer_secret'] = ''
    keys['bearer_token'] = ''
    keys['access_token_key'] = ''
    keys['access_token_secret'] = ''
    with open('./config.txt', 'r') as f:
        for line in f.readlines():
            text = line.split('=')
            text[0] = text[0].replace(' ', '')
            text[1] = text[1].replace(' ', '')
            text[1] = text[1].replace('\n', '')
            text[1] = text[1].replace("'", '')
            keys[text[0]] = text[1]
            # print(text)
    f.close

    api = TwitterAPI(keys['consumer_key'], keys['consumer_secret'], keys['access_token_key'], keys['access_token_secret'])
    keyword = request.json['keyword']
    count = int(request.json['count'])
    # keyword = "Test"
    # count = 10

    r = api.request('search/tweets', {'q':keyword, 'count':count})
    # print(r.text)
    users = {}
    tweets = {}
    for item in r:
    # print(item)
#     print(item['user']['name'])
        if(item['user']['name'] not in users):
            users[item['user']['name']] = {}
            users[item['user']['name']]['uid'] = item['user']['screen_name']
            users[item['user']['name']]['name'] = item['user']['name']
            users[item['user']['name']]['avatarURL'] = item['user']['profile_image_url_https']
            users[item['user']['name']]['tweets'] = [item['id']]
        else:
            users[item['user']['name']]['tweets'].append(item['id'])
        tweets[item['id']] = {} 
        tweets[item['id']]['id'] = item['id_str']
        tweets[item['id']]['text'] = item['text']
        tweets[item['id']]['author'] = item['user']['name']
        tweets[item['id']]['timestamp'] = item['created_at']
        tweets[item['id']]['likes'] = []
        tweets[item['id']]['replies'] = [item['user']['screen_name']]
        
        if item['in_reply_to_status_id'] != None:
            tweets[item['id']]['replyingTo'] = item['in_reply_to_status_id']
        else:
            tweets[item['id']]['replyingTo'] = None
    filenames = ['users', 'tweets']
    dicts = {}
    dicts['users'] = users
    dicts['tweets'] = tweets
    dicts['orig'] = request.json
    # print(users)
    # print(tweets)
    # for filename in filenames:
    #     if not os.path.exists('../src/source/' + filename + '.json'):
    #         open('../src/source/' + filename + '.json', 'w').close()
    #     with open('../src/source/' + filename + '.json', 'w', encoding="utf-8") as file:
    #         json.dump(dicts[filename], file)
    # print('done')
    # sys.stdout.flush()
    return dicts

