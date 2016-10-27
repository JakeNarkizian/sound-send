import os
import unittest

from server import BASE_URL
from server.channel import NoSuchChannelError
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
        with open(os.path.join(os.getcwd(), segmenter.segment_path(1)), 'rb') as readable:
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
            with open(os.path.join(os.getcwd(), segmenter.segment_path(i+1)), 'rb') as readable:
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

    def test_iterative_cleanup(self):
        segmenter = StreamSegmenter(self.channel.name)
        for i in range(StreamSegmenter.MAX_SEG_FILES):
            segmenter.add_segment(os.urandom(8))
        self.assertEqual(segmenter.smallestseg, 1)
        self.assertEqual(segmenter.segfilecnt, StreamSegmenter.MAX_SEG_FILES)
        segmenter.add_segment(os.urandom(8))
        self.assertEqual(segmenter.smallestseg, 1 + StreamSegmenter.SEG_FILE_REDUCE_BY)
        self.assertEqual(segmenter.segfilecnt, StreamSegmenter.MAX_SEG_FILES
                                               - StreamSegmenter.SEG_FILE_REDUCE_BY
                                               + 1)
        for i in range(StreamSegmenter.MAX_SEG_FILES):
            segmenter.add_segment(os.urandom(8))
        self.assertGreaterEqual(StreamSegmenter.MAX_SEG_FILES, segmenter.segfilecnt)
