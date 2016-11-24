import uuid as UUID
import shutil
from contextlib import contextmanager

import flask
import os
import json
from channel import Channel, ChannelCreationError, ChannelManager, NoSuchChannel, \
    UnauthorizedChannelRequest
from server.stream import NoSuchSegment, NoSuchSegmentOnDisk

server = flask.Flask(__name__)

channels = ChannelManager()

class ExceptionHandler(object):
    """
    This is a convenience class that handles all exceptions defined in handle so that code
    duplication can be minimized.
    """
    def __init__(self):
        self._response = None
        self._to_set = {}
        super(ExceptionHandler, self).__init__()

    @property
    def response(self):
        for k,v  in self._to_set.items():
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
            self._response = flask.Response(*args, **kwargs)#self._response = flask.Response("Invalid UUID for '%s'." % e.message, status=403,
            #                                mimetype='text/plain')
            #TODO: should we remove the UUID or uncomment the above check?
        except ChannelCreationError as e:
            self._response = flask.Response("Invalid channel name '%s'." % e.message, status=400,
                                            mimetype='text/plain')
        except NoSuchSegment as e:
            self._response = flask.Response("The segment '%s' does not exist." % e.message,
                                            status=404, mimetype='text/plain')
        except NoSuchSegmentOnDisk as e:
            self._response = flask.Response("The segment '%s' does not exist on disk. "
                                            "It may be too old." % e.message,
                                            status=410, mimetype='text/plain')
        else:
            self._response = flask.Response(*args, **kwargs)

    def set_response_attr(self, **kwargs):
        """
        Any keyword args are used to override attributes of the response.
        """
        for k, v in kwargs.items():
            self._to_set[k] = v

# Channel Manager methods
@server.route('/%s/create/<name>/<uuid>' % Channel.RESERVED_NAME)
def create_channel_request(name, uuid):
    handler = ExceptionHandler()
    with handler.handle("Channel '%s' created." % name, status=201, mimetype='text/plain'):
        channels.create(name, uuid)
    return handler.response


@server.route('/%s/destroy/<name>/<uuid>' % Channel.RESERVED_NAME)
def destroy_channel_request(name, uuid):
    handler = ExceptionHandler()
    with handler.handle("Channel '%s' destroyed." % name, status=200, mimetype='text/plain'):
        channels.remove(name, uuid)
    return handler.response

@server.route('/%s/active' % Channel.RESERVED_NAME)
def active_channel_request():
    handler = ExceptionHandler()
    with handler.handle(status=200, mimetype='application/json'):
        handler.set_response_attr(data=json.dumps(channels.active_channels))
    return handler.response

# Channel specific methods for listener
@server.route('/<name>/index.json')
def channel_index_request(name):
    handler = ExceptionHandler()
    with handler.handle(status=200, mimetype='application/x-mpegURL'):
        handler.set_response_attr(data=channels[name].index())
    return handler.response


@server.route('/<name>/segs/<int:i>.m4a')
def channel_segment_request(name, i):
    handler = ExceptionHandler()
    with handler.handle(status=200, mimetype='audio/mp4'):
        handler.set_response_attr(data=channels[name].segment(i))
    return handler.response

# Channel specific methods for broadcaster
@server.route('/<name>/<uuid>/listener_count')
def channel_listener_count_request(name, uuid):
    handler = ExceptionHandler()
    with handler.handle(status=200, mimetype='application/json'):
        handler.set_response_attr(data=json.dumps(dict(count=channels[name].listeners)))
    return handler.response

@server.route('/<name>/<uuid>/add_segment', methods=['POST'])
def channel_add_segment(name, uuid):
    handler = ExceptionHandler()
    with handler.handle():
        channel = channels[name]
        channel.stream.add_segment(flask.request.data)
    return handler.response


def main():
    tempdir = os.path.join(os.getcwd(), str(UUID.uuid4()))
    os.mkdir(tempdir)
    try:
        os.chdir(tempdir)
        server.run()
    finally:
        shutil.rmtree(tempdir)

if __name__ == "__main__":
    main()
