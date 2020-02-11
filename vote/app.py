from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json



option_a = os.getenv('OPTION_A', "true")
option_b = os.getenv('OPTION_B', "false")
hostname = socket.gethostname()
counter = 1

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['GET', 'POST'])
def index():
    voter_id = request.cookies.get('voter_id')
    voter_name = request.cookies.get('voter_name')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    if not voter_name:
        voter_name = ""

    if request.method == 'POST':
        voter_name = request.form['player']

    resp = make_response(render_template(
        'index.html',
        hostname=hostname,
        name=voter_name
    ))
    resp.set_cookie('voter_id', voter_id)
    resp.set_cookie('voter_name', voter_name)
    return resp

@app.route("/start", methods=['POST','GET'])
def start():
    count = counter
    question = os.getenv('QUESTION_' + str(count), "Question")
    voter_id = request.cookies.get('voter_id')

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote, 'question': question})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'vote.html',
        question=question,
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    return resp

@app.route("/next", methods=['POST','GET'])
def next():
    count = counter + 1
    question = os.getenv('QUESTION_' + str(count), "Question")
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote, 'question': question})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'vote.html',
        question=question,
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
