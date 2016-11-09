import shutil

import os
from server.stream import StreamSegmenter
import logging

log = logging.getLogger(__name__)

class ChannelCreationError(Exception):
    pass


class Channel(object):

    RESERVED_NAME = 'channelmanager'
    def __init__(self, name, broadcasterUUID):
        """
        :param str name: The name of the channel. A channel of the same name must not exist on the
            disk. Also the name must not match the RESERVED_NAME constant.
        :param str broadcasterUUID: A practically unique string that is used to identify the owner.
        """
        if name == self.RESERVED_NAME:
            raise ChannelCreationError()
        else:
            self.name = name
            self.broadcasterUUID = broadcasterUUID
            self._dir_path = os.path.join(os.getcwd(), name)
            try:
                os.mkdir(self._dir_path)
            except OSError:
                log.exception('')
                raise ChannelCreationError()

        self.stream = StreamSegmenter(self.name)
        super(Channel, self).__init__()

    def destory(self):
        """
        This destructor method removed the channel directory.
        """
        try:
            shutil.rmtree(self._dir_path)
        finally:
            pass # TODO: this should alert listeners that the channel has been closed
