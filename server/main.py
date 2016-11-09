import uuid
import shutil
import flask
import os
from channel import Channel, ChannelCreationError

server = flask.Flask(__name__)

channels = {}

@server.route('/%s/createchannel/<name>/<uuid>' % Channel.RESERVED_NAME)
def create_channel_request(name, uuid):
    try:
        channel = Channel(name, uuid)
    except ChannelCreationError:
        flask.abort(400)
    else:
        channels[name] = channel
        return flask.render_template('page.html'), 201

@server.route('/<name>/destorychannel/<uuid>')
def destroy_channel(name, uuid):
    try:
        channel = channels[name]
    except KeyError:
        flask.abort(410)
    else:
        if channel.broadcasterUUID != uuid:
            flask.abort(403)
        else:
            channel.destory()
            del channels[name]
            return flask.render_template('page.html'), 200

if __name__ == "__main__":
    tempdir = os.path.join(os.getcwd(), str(uuid.uuid4()))
    os.mkdir(tempdir)
    try:
        os.chdir(tempdir)
        server.run()
    finally:
        shutil.rmtree(tempdir)
