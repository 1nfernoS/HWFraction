import traceback
from json import JSONDecodeError
from threading import Thread

import settings
import vk_api
import flask
from flask import Flask, request, json, make_response
import commands

# distribution
# targets
# keyboards
# squads
# battle results
# Remind before battle
# Customize texts
# chats are 2000000000+

app = Flask(__name__)


@app.route('/')
def index():
    return '<h2>HWHelper Bot, use VK bot instead this</h2>'


@app.route('/', methods=['POST'])
def handler():
    try:
        r = request.data
        data = json.loads(r)
    except JSONDecodeError:
        return make_response("No data provided", 400)

    # confirmation don't send any other data
    try:
        type_msg = data['type']
    except KeyError:
        return make_response("Wrong data provided", 400)
    except TypeError:
        print(data)
        return 'bad'

    if type_msg == 'confirmation':
        return settings.confirmation_token

    try:
        obj_msg = data['object']
        group_id = data['group_id']
    except KeyError:
        return make_response("Wrong data provided", 400)

    if group_id != settings.group_id:
        return make_response("Error: only bot have access", 403)

    if type_msg == 'message_new':
        data_msg = obj_msg['message']
        message(data_msg)

    return make_response('ok', 200)


@app.errorhandler(500)
def internal_error():
    print("\n\n\n500 error caught\n\n\n")
    print(traceback.format_exc())


def message(msg):
    t_msg = {'date': 1615112840, 'from_id': 260894984, 'id': 0, 'out': 0, 'peer_id': 2000000002, 'text': '/target 5',
             'conversation_message_id': 21666, 'fwd_messages': [], 'important': False, 'random_id': 0,
             'attachments': [], 'is_hidden': False}

    time = int(msg['date'])
    text = str(msg['text'])
    chat = int(msg['peer_id'])
    user = int(msg['from_id'])

    if settings.old_msg['message'] == text and settings.old_msg['time'] == time:
        vk_api.send(chat, "2fast4me")
    else:
        settings.old_msg['message'] = text
        settings.old_msg['time'] = time

    # forwards
    if len(msg['fwd_messages']) != 0 and text == '':
        fwd = msg['fwd_messages']
        # if 1 without anything, return time (for now)
        if len(fwd) == 1:
            try:
                fwd_time = str(msg['fwd_messages'][0]['fwd_messages'][0]['date']) + '\n'
            except KeyError:
                fwd_time = str(msg['fwd_messages'][0]['date']) + '\n'

            vk_api.send(chat, str(fwd_time))
            return
        # 6 msg for fractions and 1 for results. Must be bot id
        if len(fwd) == 7:
            dist = ''
            for i in range(7):
                if fwd[i]['from_id'] == -172959149:
                    dist += str(fwd[i]['text']).replace('\n\n', '\n') + '\n\n'
                else:
                    vk_api.send(chat, "Error in forwards")
                    return
            vk_api.send(chat, dist)
            return
        return

    # commands
    # TODO: '/' commands only in chats
    if msg['text'].startswith('/'):
        if user in settings.LO:
            command = msg['text'].split()
            command[0] = command[0].replace('/', '')
            if command[0] in dir(commands):
                # vk_api.send(chat, '\"/' + str(command[0])+'\" in list')
                commands.start(msg, command[0])
                # need to call somehow
            else:
                vk_api.send(chat, '\"/' + str(command[0]) + '\" not in list')
            return
        else:
            vk_api.send(chat, "Access Denied")
        return


if __name__ == '__main__':
    app.run()
