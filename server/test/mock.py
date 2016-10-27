import shutil
import os


class MockChannel(object):
    @classmethod
    def create(cls, name):
        channel = cls(name)
        os.mkdir(name)
        return channel

    def destroy(self):
        path = os.path.join(os.getcwd(), self.name)
        assert path != os.getcwd()
        shutil.rmtree(path)

    def __init__(self, name):
        self.name = name
        super(MockChannel, self).__init__()


