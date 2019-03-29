from wxpy import *

# 扫描登录
bot = Bot(cache_path=True)

# 获取所有好友
friends = bot.friends()
# 获取所有聊天群,更新微信群列表
groups = bot.groups(update=True, contact_only=False)
print(friends)
print(type(friends))
print(type(groups))
print(groups)

'''

找出名字包括“小绵纺-报警群”的群。假设我们有2个微信群，
分别叫“小绵纺-报警群1群”、“小绵纺-报警群2群”。
如果有3个或以上的小绵纺-报警群，上面这句代码也能全部找出来，
并在后面的代码中实现多群同步

'''
# my_groups = groups.search(u'小绵纺-报警群')
# my_groups1 = groups.search(u'蓝色期待-报警群')

# 更新群聊的信息
# g = my_groups[0].update_group(members_details=True)

# friend = friends.search(u'Deng~')[0]
friend = friends.search(u'肥猫')[0]


# 注册消息响应事件，一旦收到小绵纺-报警群的消息，就执行下面的代码同步消息。机器人自己在群里发布的信息也进行同步
@bot.register(except_self=False)
def sync_my_groups(msg):
    # prefix = msg.member.name + ':'
    # suffix = '---->' + msg.member.name

    # if not msg.member:

    text = msg.text
    friend.send(u""+text)

    print(msg)
    print(type(msg))
    # print(prefix)

    # 同步“小绵纺-报警群1群”和“小绵纺-报警群2群”的消息。包括文字、图片、视频、语音、文件、分享、普通表情、地图等。
    # sync_message_in_groups(msg, my_groups, prefix=my_name)

    # try:
    #     # 消息同步到其它群，不能同步本群
    #     sync_message_in_groups(msg, my_groups1, prefix=prefix, suffix=suffix)
    # except Exception as e:
    #     print(e)


# 历史消息搜索
sent_msgs = bot.messages.search(sender=bot.self)
print(sent_msgs)

# 向机器人的文件传输助手发送消息“Hello”
bot.file_helper.send('Hello')

# 堵塞进程，直到结束消息监听 (例如，机器人被登出时)，让机器人保持运行
bot.join()

# print(end='')

# @bot.register()
# def reply_msg(msg):
#     msg.reply(u'噶蛤玩意？')
#
#
# embed()
