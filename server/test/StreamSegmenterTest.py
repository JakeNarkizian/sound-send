import random
import time

import os
import unittest

from server import BASE_URL
from server import NoSuchChannelError
from server.stream import StreamSegmenter
from server.test.mock import MockChannel


class StreamSegmenterTest(unittest.TestCase):
    def setUp(self):
        self.channel = MockChannel.create('testchannel')

    def tearDown(self):
        self.channel.destroy()

    def test_invalid_channel(self):
        try:
            StreamSegmenter('invalidChannel')
        except NoSuchChannelError:
            pass
        else:
            self.fail('No exception was raised.')

    def test_seg_cleanup_with_max_segs(self):
        segmenter = StreamSegmenter(self.channel.name)
        for i in range(StreamSegmenter.MAX_SEGS_ON_DISK):
            segmenter.add_segment(os.urandom(8))
            time.sleep(1)  # sleep between files to prevent the time stamps from being the same
        self.assertEqual(self._oldest_seg_on_disk(segmenter), '1.m4a')
        self.assertEqual(len(os.listdir(segmenter.seg_dir_abspath)),
                         StreamSegmenter.MAX_SEGS_ON_DISK)

    def test_seg_cleanup_with_max_segs_plus_one(self):
        segmenter = StreamSegmenter(self.channel.name)
        for i in range(StreamSegmenter.MAX_SEGS_ON_DISK + 1):
            segmenter.add_segment(os.urandom(8))
            time.sleep(1)  # sleep between files to prevent the time stamps from being the same
        self.assertEqual(self._oldest_seg_on_disk(segmenter),
                         '%d.m4a' % (1 + StreamSegmenter.SEG_FILE_REDUCE_BY))
        self.assertEqual(len(os.listdir(segmenter.seg_dir_abspath)),
                         StreamSegmenter.MAX_SEGS_ON_DISK - StreamSegmenter.SEG_FILE_REDUCE_BY + 1)

    def test_seg_cleanup_with_max_segs_plus_random(self):
        segmenter = StreamSegmenter(self.channel.name)
        for i in range(StreamSegmenter.MAX_SEGS_ON_DISK
                               + random.randint(2, 2 * StreamSegmenter.MAX_SEGS_ON_DISK)):
            segmenter.add_segment(os.urandom(8))
        self.assertGreaterEqual(StreamSegmenter.MAX_SEGS_ON_DISK,
                                len(os.listdir(segmenter.seg_dir_abspath)))

    def _oldest_seg_on_disk(self, segmenter):
        segs_on_disk = os.listdir(segmenter.seg_dir_abspath)
        segs_on_disk.sort(key=lambda x: os.path.getctime(segmenter.seg_abspath_from_string(x)),
                          reverse=True)
        return segs_on_disk.pop()