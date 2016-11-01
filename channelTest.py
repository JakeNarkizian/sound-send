from channel import ChannelManager
from pkg_resources import get_distribution

manager = ChannelManager()
manager.create_new_channel("test1","abc123")
manager.create_new_channel("test2","xyz456")
manager.create_new_channel("test3","hello")

manager.add_user("test1","man1")
manager.add_user("test1","man2")
manager.add_user("test1","man3")
manager.add_user("test1","man4")

manager.add_user("test2","man5")

manager.add_user("test2","man5")
manager.add_user("test3","man6")
manager.add_user("test3","man1")
#manager.add_user("testX","man5") -- bad case

manager.remove_user("test1","man1")
manager.remove_user("test1","man6")
#manager.remove_user("testX","man1") -- bad case

print(manager.check_user("man2"))
print(manager.check_user("man7"))

manager.generate_metadata("test1")
