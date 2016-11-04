import uuid
import shutil
import flask
import os
from channel import Channel
server = flask.Flask(__name__)

@server.route('/channelManager/createChannel/<name>/<uuid>')
def create_channel_request(name, uuid):
    try:
        Channel(name, uuid)
    except OSError:
        flask.abort(400)
    return flask.render_template('page.html'), 201

if __name__ == "__main__":
    tempdir = os.path.join(os.getcwd(), str(uuid.uuid4()))
    os.mkdir(tempdir)
    os.chdir(tempdir)
    try:
        server.run()
    finally:
        shutil.rmtree(tempdir)
