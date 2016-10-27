import os

from server import BASE_URL
from server.channel import NoSuchChannelError


class StreamSegmenter(object):
    MAX_SEG_FILES = 16
    SEG_FILE_REDUCE_BY = 4
    def __init__(self, channelName, seglen=10):
        channelPath = os.path.join(os.getcwd(), channelName)
        self.segpath = '%s/segs' % channelName
        if not os.path.exists(channelPath):
            raise NoSuchChannelError()
        else:
            os.mkdir(self.segpath)
        self.seglen = seglen
        self.channelname = channelName
        self.segcnt = 0
        self.segfilecnt = 0
        self.smallestseg = 1
        super(StreamSegmenter, self).__init__()

    def add_segment(self, segmentData):
        """
        Adds a segment to the current stream.
        :return:
        """
        if self.segfilecnt == self.MAX_SEG_FILES:
            for i in range(self.SEG_FILE_REDUCE_BY):
                os.remove(os.path.join(os.getcwd(), self.segment_path(self.smallestseg + i)))
            self.segfilecnt -= self.SEG_FILE_REDUCE_BY
            self.smallestseg += self.SEG_FILE_REDUCE_BY
        assert self.segfilecnt < self.MAX_SEG_FILES
        with open(os.path.join(os.getcwd(), self.segment_path(self.segcnt+1)), 'wb') as writable:
            writable.write(segmentData)
        self.segcnt += 1
        self.segfilecnt += 1

    def get_current_index(self):
        """
        This file should have a .M3U8 extension

        For details about the formatting of this string see:
            https://tools.ietf.org/html/draft-pantos-http-live-streaming-20
        """
        # header
        s  = "#EXT-X-VERSION:3\n"  # defines protocol version
        s += "#EXTM3U\n"
        s += "#EXT-X-TARGETDURATION:%s\n" % self.seglen
        s += "#EXT-X-MEDIA-SEQUENCE:1\n\n"
        # body
        for i in range(self.segcnt):
            s += "#EXTINF:%.3f,\n" % self.seglen
            s += "http://%s/%s\n" % (BASE_URL, self.segment_path(i+1))
        # footer
        s += "#EXT-X-ENDLIST\n"
        return s

    def segment_path(self, i):
        return '%s/%d.ts' % (self.segpath, i)
