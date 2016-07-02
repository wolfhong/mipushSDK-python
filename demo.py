# -*- coding: utf-8 -*-
from mipush.httpbase import MipushClient, MipushError
from mipush.message import Message

APPSECRET = 'your app secret'
PACKAGE_ANDROID = 'Android设备,传入App的包名'
PACKAGE_IOS = 'IOS设备,传入App的Bundle Id'

# sandbox API只提供对IOS支持，不支持Android。
client = MipushClient('release', APPSECRET, retries=1, timeout=3)
message = Message()
message.build(PACKAGE_ANDROID, u'标题', u'内容')
# 向所有设备发送消息
# result = client.broadcastAll(message)

try:
    result = client.checkScheduleJobExist('not-exist-job')
    # result = client.getInvalidRegIds()
    print result.raw
except MipushError as e:
    print 'error'
    print e.raw
