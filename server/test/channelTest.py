import unittest
import uuid as UUID
import os
from server.channel import Channel, ChannelCreationError, ChannelManager, UnauthorizedChannelRequest


class ChannelTest(unittest.TestCase):
    def test_channel_with_reserved_name(self):
        try:
            Channel(Channel.RESERVED_NAME, str(UUID.uuid4()))
        except ChannelCreationError:
            pass
        else:
            self.fail('Channel was created with reserved name.')

    def test_channel_creation(self):
        channel = Channel('test-channel-creation', str(UUID.uuid4()))
        try:
            self.assertTrue(os.path.exists(channel._dir_path))
        finally:
            channel.destroy()

    def test_duplicate_channel_creation(self):
        name = 'test-channel-duplicate'
        channel1 = Channel(name, str(UUID.uuid4()))
        try:
            channel2 = Channel(name, str(UUID.uuid4()))
        except ChannelCreationError:
            pass
        else:
            channel2.destroy()
            self.fail('Duplicate channel was created.')
        finally:
            channel1.destroy()

    def test_channel_destroy(self):
        channel = Channel('test-channel-destroy', str(UUID.uuid4()))
        self.assertTrue(os.path.exists(channel._dir_path))
        channel.destroy()
        self.assertFalse(os.path.exists(channel._dir_path))


class ChannelManagerTest(unittest.TestCase):

    def test_get_item(self):
        manager = ChannelManager()
        name = 'test-channel-manager-get-item'
        uuid = str(UUID.uuid4())
        manager.create(name, uuid)
        try:
            _ = manager[name]
            _ = manager[name, uuid]
            try:
                _ = manager[name, str(UUID.uuid4())]
            except UnauthorizedChannelRequest:
                pass
            else:
                self.fail('Unauthorized channel access what allowed.')
        finally:
            manager.remove(name, uuid)
