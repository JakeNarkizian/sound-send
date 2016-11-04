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

    def test_empty_index(self):
        segmenter = StreamSegmenter(self.channel.name)
        self.assertEqual(segmenter.get_current_index(),
                         '#EXT-X-VERSION:3\n'
                         '#EXTM3U\n'
                         '#EXT-X-TARGETDURATION:10\n'
                         '#EXT-X-MEDIA-SEQUENCE:1\n'
                         '\n'
                         '#EXT-X-ENDLIST\n')

    def test_one_segment(self):
        segmenter = StreamSegmenter(self.channel.name)
        data = os.urandom(32)  # gets 32 random bytes
        segmenter.add_segment(data)
        with open(os.path.join(os.getcwd(), segmenter.seg_abspath_from_index(1)), 'rb') as readable:
            self.assertEqual(readable.read(), data)
        self.assertEqual(segmenter.get_current_index(),
                         '#EXT-X-VERSION:3\n'
                         '#EXTM3U\n#'
                         'EXT-X-TARGETDURATION:10\n'
                         '#EXT-X-MEDIA-SEQUENCE:1\n'
                         '\n'
                         '#EXTINF:10.000,\n'
                         'http://%s/%s/segs/1.ts\n'
                         '#EXT-X-ENDLIST\n' % (BASE_URL, self.channel.name))

    def test_five_segments(self):
        segmenter = StreamSegmenter(self.channel.name)
        data = []
        for i in range(5):
            data.append(os.urandom(32))  # gets 32 random bytes
            segmenter.add_segment(data[i])
            with open(os.path.join(os.getcwd(), segmenter.seg_abspath_from_index(i+1)), 'rb') as readable:
                self.assertEqual(readable.read(), data[i])
        self.assertEqual(segmenter.get_current_index(),
                         '#EXT-X-VERSION:3\n'
                         '#EXTM3U\n#'
                         'EXT-X-TARGETDURATION:10\n'
                         '#EXT-X-MEDIA-SEQUENCE:1\n'
                         '\n'
                         '#EXTINF:10.000,\n'
                         'http://{baseurl}/{channel}/segs/1.ts\n'
                         '#EXTINF:10.000,\n'
                         'http://{baseurl}/{channel}/segs/2.ts\n'
                         '#EXTINF:10.000,\n'
                         'http://{baseurl}/{channel}/segs/3.ts\n'
                         '#EXTINF:10.000,\n'
                         'http://{baseurl}/{channel}/segs/4.ts\n'
                         '#EXTINF:10.000,\n'
                         'http://{baseurl}/{channel}/segs/5.ts\n'
                         '#EXT-X-ENDLIST\n'.format(baseurl=BASE_URL, channel=self.channel.name))

    def test_seg_cleanup_with_max_segs(self):
        segmenter = StreamSegmenter(self.channel.name)
        for i in range(StreamSegmenter.MAX_SEGS_ON_DISK):
            segmenter.add_segment(os.urandom(8))
            time.sleep(1)  # sleep between files to prevent the time stamps from being the same
        self.assertEqual(self._oldest_seg_on_disk(segmenter), '1.ts')
        self.assertEqual(len(os.listdir(segmenter.seg_dir_abspath)),
                         StreamSegmenter.MAX_SEGS_ON_DISK)

    def test_seg_cleanup_with_max_segs_plus_one(self):
        segmenter = StreamSegmenter(self.channel.name)
        for i in range(StreamSegmenter.MAX_SEGS_ON_DISK + 1):
            segmenter.add_segment(os.urandom(8))
            time.sleep(1)  # sleep between files to prevent the time stamps from being the same
        self.assertEqual(self._oldest_seg_on_disk(segmenter),
                         '%d.ts' % (1 + StreamSegmenter.SEG_FILE_REDUCE_BY))
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