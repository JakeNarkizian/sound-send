import shutil
import os
from server.stream import StreamSegmenter
import logging

log = logging.getLogger(__name__)

class ChannelCreationError(Exception):
    pass


class NoSuchChannel(Exception):
    pass


class UnauthorizedChannelRequest(Exception):
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
            raise ChannelCreationError(name)
        else:
            self.name = name
            self.uuid = broadcasterUUID
            self._dir_path = os.path.join(os.getcwd(), name)
            try:
                os.mkdir(self._dir_path)
            except OSError:
                log.exception('')
                raise ChannelCreationError(name)

        self.stream = StreamSegmenter(self.name)
        super(Channel, self).__init__()

    def destroy(self):
        """
        This destructor method removed the channel directory.
        """
        try:
            shutil.rmtree(self._dir_path)
        finally:
            pass # TODO: this should alert listeners that the channel has been closed

    def index(self):
        return self.stream.get_current_index()

class ChannelManager(object):
    def __init__(self):
        self._channels = dict()
        super(ChannelManager, self).__init__()

    def __getitem__(self, item):
        """
        Allows the manager to be queried for channels like a dictionary. The parameter item must be
        either the name of a channel as a string or a tuple of the form (<channel name>, <uuid>).
        """
        if isinstance(item, tuple):
            name = item[0]
            uuid = item[1]
        else:
            name = item
            uuid = None
        return self._get_channel(name, uuid=uuid)

    def _get_channel(self, name, uuid=None):
        try:
            channel = self._channels[name]
        except KeyError:
            raise NoSuchChannel(name)
        else:
            if uuid is not None and channel.uuid != uuid:
                log.info("The UUID '%s' is not the UUID of channel '%s'", uuid, name)
                raise UnauthorizedChannelRequest(name)
            else:
                return channel

    def create(self, name, uuid):
        channel = Channel(name, uuid)
        self._channels[name] = channel

    def remove(self, name, uuid):
        self._get_channel(name, uuid=uuid).destroy()
        del self._channels[name]
