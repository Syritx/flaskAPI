from flask import Flask, render_template
from datetime import datetime

import subprocess
import json

app = Flask(__name__)
isPartActive = False
message = ''

json_file = '{ "active": false }'

logs = ['']

@app.route('/')
def apiMain():
    return render_template('index.html',part_active='Status: ' + 'inactive'.upper(), content=logs)

@app.route("/button/", methods=['POST'])
def togglePart():
    global isPartActive, message, json_file, logs
    isPartActive = not isPartActive
    
    # writing a new log by a button press
    if isPartActive:
        message = 'active'
        log = str(datetime.now().strftime("%H:%M:%S"))+' Status: active'
        logs.append(log)

    else:
        message = 'inactive'
        log = str(datetime.now().strftime("%H:%M:%S"))+' Status: inactive'
        logs.append(log)
    
    # reversing logs (recent to oldest)
    new_logs = []
    for x in range(len(logs)-1, 0, -1):
        new_logs.append(logs[x])
    
    # gets 10 recent logs
    completed_logs = []
    for x in range(len(new_logs)-1):
        if (len(new_logs)-x > len(new_logs)-10):
            completed_logs.append(new_logs[x])
    
    # creating json file
    json_file = '{ \"active\": '+str(isPartActive).lower()+' }'
    
    # rendering html
    return render_template('index.html',part_active='Status: ' + message.upper(), content=completed_logs)

# API page
@app.route('/api')
def api():
    global json_file
    return json_file

app.run(debug=True)
