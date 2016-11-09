import unittest
import uuid

import os
from server.channel import Channel, ChannelCreationError


class channelTest(unittest.TestCase):
    def test_channel_with_reserved_name(self):
        try:
            Channel(Channel.RESERVED_NAME, str(uuid.uuid4()))
        except ChannelCreationError:
            pass
        else:
            self.fail('Channel was created with reserved name.')

    def test_channel_creation(self):
        channel = Channel('test', str(uuid.uuid4()))
        try:
            self.assertTrue(os.path.exists(channel._dir_path))
        finally:
            channel.destory()

    def test_duplicate_channel_creation(self):
        name = 'test'
        channel1 = Channel(name, str(uuid.uuid4()))
        try:
            channel2 = Channel(name, str(uuid.uuid4()))
        except ChannelCreationError:
            pass
        else:
            channel2.destory()
            self.fail('Duplciate channel was created.')
        finally:
            channel1.destory()

    def test_channel_destroy(self):
        channel = Channel('test', str(uuid.uuid4()))
        self.assertTrue(os.path.exists(channel._dir_path))
        channel.destory()
        self.assertFalse(os.path.exists(channel._dir_path))

