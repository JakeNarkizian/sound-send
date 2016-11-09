import uuid
import shutil
import flask
import os
from channel import Channel, ChannelCreationError

server = flask.Flask(__name__)


@server.route('/%s/createchannel/<name>/<uuid>' % Channel.RESERVED_NAME)
def create_channel_request(name, uuid):
    try:
        Channel(name, uuid)
    except ChannelCreationError:
        flask.abort(400)
    else:
        return flask.render_template('page.html'), 201

if __name__ == "__main__":
    tempdir = os.path.join(os.getcwd(), str(uuid.uuid4()))
    os.mkdir(tempdir)
    os.chdir(tempdir)
    try:
        server.run()
    finally:
        shutil.rmtree(tempdir)
