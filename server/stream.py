import os

from server import BASE_URL
from server import NoSuchChannelError
import logging

log = logging.getLogger(__name__)


class NoSuchSegmentOnDisk(Exception):
    pass


class NoSuchSegment(Exception):
    pass


class StreamSegmenter(object):
    MAX_SEGS_ON_DISK = 16
    SEG_FILE_REDUCE_BY = 4
    MAX_SEG_LEN = 10
    def __init__(self, channelName, seglen=10):
        channel_path = os.path.join(os.getcwd(), channelName)
        if not os.path.exists(channel_path):
            raise NoSuchChannelError
        else:
            self.seg_dir_abspath = os.path.join(channel_path, 'segs')
            os.mkdir(self.seg_dir_abspath)
            self.channel_name = channelName
            self.total_segs = 0
            super(StreamSegmenter, self).__init__()

    def add_segment(self, segmentData):
        """
        Adds a segment to the current stream.
        :return:
        """
        segs_on_disk = os.listdir(self.seg_dir_abspath)
        if len(segs_on_disk) >= self.MAX_SEGS_ON_DISK:
            log.debug('Disk segment overflow for channel %s. Deleting oldest %d segments.',
                      self.channel_name, self.SEG_FILE_REDUCE_BY)
            # sort list by modification time from youngest to oldest
            segs_on_disk.sort(key=lambda x: os.path.getmtime(self.seg_abspath_from_string(x)),
                              reverse=True)
            for i in range(self.SEG_FILE_REDUCE_BY):
                os.remove(self.seg_abspath_from_string(segs_on_disk.pop()))

        assert len(segs_on_disk) < self.MAX_SEGS_ON_DISK
        with open(self.seg_abspath_from_index(self.total_segs+1), 'wb') as writable:
            writable.write(segmentData)
        self.total_segs += 1
        log.debug('Added segment %d to %s', self.total_segs, self.channel_name)

    def get_segment(self, i):
        """
        Returns the bytes of the given segment if the segment file exists on the disk.
        """
        if i > self.total_segs:
            # This should never happen
            raise NoSuchSegment(str(i))
        else:
            try:
                with open(self.seg_abspath_from_index(i), 'rb') as readable:
                    return readable.read()
            except IOError:
                raise NoSuchSegmentOnDisk(str(i))

    def get_current_index(self):
        """
        For details about the formatting of this string see:
            https://tools.ietf.org/html/draft-pantos-http-live-streaming-20
        """
        # header
        s  = "#EXT-X-VERSION:3\n"  # defines protocol version
        s += "#EXTM3U\n"
        s += "#EXT-X-TARGETDURATION:%s\n" % self.MAX_SEG_LEN
        s += "#EXT-X-MEDIA-SEQUENCE:1\n\n"
        # body
        for i in range(self.total_segs):
            s += "#EXTINF:%.3f,\n" % self.MAX_SEG_LEN
            s += "http://%s/%s/segs/%d.ts\n" % (BASE_URL, self.channel_name, i+1)
        # footer
        s += "#EXT-X-ENDLIST\n"
        return s

    def seg_abspath_from_index(self, i):
        return self.seg_abspath_from_string('%d.ts' % i)

    def seg_abspath_from_string(self, s):
        return os.path.join(self.seg_dir_abspath, s)
