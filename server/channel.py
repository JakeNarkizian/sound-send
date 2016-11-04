import os
from server.stream import StreamSegmenter
import logging

log = logging.getLogger(__name__)

class ChannelCreationError(Exception):
    pass


class Channel(object):
    def __init__(self, name, broadcasterUUID):
        self.name = name
        self.broadcasterUUID = broadcasterUUID
        self.listeners = []
        os.mkdir(os.path.join(os.getcwd(), name))
        self.stream = StreamSegmenter(self.name)
        super(Channel, self).__init__()

    num_listeners = property(lambda self: len(self.listeners))
