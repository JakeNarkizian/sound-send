import json

class NoSuchChannelError(Exception):
    pass

class ChannelCreationError(Exception):
    pass

class Channel(object):

    @classmethod
    def create(cls):
        """
        Creates a new channel.
        """
        pass

    def __init__(self, name, broadcasterUUID):
        self.name = name
        self.broadcaster = broadcasterUUID
        self.userlist = []
        self.url = "http://baseurl.com/" + name
        self.add_listener(name)
        super(Channel, self).__init__()

    num_listeners = property(lambda self: len(self.userlist))

    def add_listener(self, listener):
        if not (listener in self.userlist):
            self.userlist.append(listener)
            return True
        else:
            return False

    def remove_listener(self, listener):
        if not (listener in self.userlist):
            return False
        else:
            self.userlist.remove(listener)
            return True

    def is_in_channel(self, name):
        return (name in self.userlist)

    def is_same_uuid(self, id):
        return (self.broadcaster == id)

    def create_metadata(self):
        with open('./metadata.txt','w') as fin:
            data = {'version':1.0,
                    'name':self.name,
                    'num_listeners':self.num_listeners,
                    'url':self.url,
                    'broadcaster':self.broadcaster,
                    'user_list':self.userlist}
            json.dump(data, fin)

class ChannelManager(object):
    def __init__(self):
        self.channels = {}

    def create_new_channel(self, name, uuid):
        if name in self.channels.keys():
            raise ChannelCreationError()
        else:
            self.channels[name] = Channel(name, uuid)

    def check_user(self, name):
        for chan in self.channels:
            if self.channels[chan].is_in_channel(name):
                return True
        return False

    def add_user(self, channel, name):
        if channel in self.channels.keys():
            if not self.check_user(name):
                if self.channels[channel].add_listener(name):
                    print('User: ' + name + ' Added!')
                else:
                    print('User: ' + name + ' Was Already In Channel!')
            else:
                print('User: ' + name + ' Already Connected To Channel!')
        else:
            raise NoSuchChannelError()

    def remove_user(self, channel, name):
        if channel in self.channels.keys():
            if self.channels[channel].remove_listener(name):
                print('User: ' + name + ' Was Removed!')
            else:
                print('User: ' + name + ' Was Not Found In Channel!')
        else:
            raise NoSuchChannelError()

    def generate_metadata(self, channel):
        if channel in self.channels.keys():
            self.channels[channel].create_metadata()
        else:
            raise NoSuchChannelError()
