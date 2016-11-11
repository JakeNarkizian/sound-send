import uuid as UUID
import shutil
from contextlib import contextmanager

import flask
import os
from channel import Channel, ChannelCreationError, ChannelManager, NoSuchChannel, \
    UnauthorizedChannelRequest

server = flask.Flask(__name__)

channels = ChannelManager()

class ExceptionHandler(object):
    """
    This is a convenience class that handles all exceptions defined in handle so that code
    duplication can be minimized.
    """
    def __init__(self):
        self._response = None
        super(ExceptionHandler, self).__init__()

    def response(self, **kwargs):
        """
        Any keyword args are used to override attributes of the response.
        """
        for k,v  in kwargs.items():
            setattr(self._response, k, v)
        return self._response

    @contextmanager
    def handle(self, *args, **kwargs):
        """
        Runs the statement in yield and excepts the exceptions defined below. If an exception is
        raised self.response is set to the defined response. If no exception is raised as
        flask.Response object is created with args and kwargs.
        """
        try:
            yield
        except NoSuchChannel as e:
            self._response = flask.Response("No such channel '%s'." % e.message, status=404,
                                            mimetype='text/plain')
        except UnauthorizedChannelRequest as e:
            self._response = flask.Response("Invalid UUID for '%s'." % e.message, status=403,
                                            mimetype='text/plain')
        except ChannelCreationError as e:
            self._response = flask.Response("Invalid channel name '%s'." % e.message, status=400,
                                            mimetype='text/plain')
        else:
            self._response = flask.Response(*args, **kwargs)


@server.route('/%s/create/<name>/<uuid>' % Channel.RESERVED_NAME)
def create_channel_request(name, uuid):
    handler = ExceptionHandler()
    with handler.handle("Channel '%s' created." % name, status=201, mimetype='text/plain'):
        channels.create(name, uuid)
    return handler.response()


@server.route('/%s/destroy/<name>/<uuid>' % Channel.RESERVED_NAME)
def destroy_channel_request(name, uuid):
    handler = ExceptionHandler()
    with handler.handle("Channel '%s' destroyed." % name, status=200, mimetype='text/plain'):
        channels.remove(name, uuid)
    return handler.response()


@server.route('/<name>/index.M3U8')
def channel_index_request(name):
    handler = ExceptionHandler()
    index = ''
    with handler.handle(index, status=200, mimetype='application/x-mpegURL'):
        index = channels[name].index()
    return handler.response(data=index)


if __name__ == "__main__":
    tempdir = os.path.join(os.getcwd(), str(UUID.uuid4()))
    os.mkdir(tempdir)
    try:
        os.chdir(tempdir)
        server.run()
    finally:
        shutil.rmtree(tempdir)
