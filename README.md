## 简介
- 这是小米推送的服务端SDK，[官网上](http://dev.xiaomi.com/mipush/downpage/)并没有提供python版本的SDK,因此根据PHP版本SDK (*2.2.16版,于2016.3.28更新*) 和 *文档* 整理出来了该Python版.
- 更多信息请查看[官方文档](http://dev.xiaomi.com/doc/?p=533)


## Tips
- 根据官方文档说明：dev测试环境只提供对IOS支持，不支持Android.


## Example

    # -*- coding: utf-8 -*-
    from mipush.httpbase import MipushClient, MipushError
    from mipush.message import Message

    APPSECRET = 'your app secret'
    PACKAGE_ANDROID = 'Android设备,传入App的包名'
    PACKAGE_IOS = 'IOS设备,传入App的Bundle Id'

    APPSECRET = 'R9LeELbhXfjCqV+MCsXmIw=='
    PACKAGE_ANDROID = 'com.didiapp.banlv'

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


## 更多使用方法

    ###### DevTools #####

    ''' 获取一个应用的某个用户目前设置的所有Alias '''
    client.getAliasesOf(packagename, regid)

    ''' 获取一个应用的某个用户目前订阅的所有Topic '''
    client.getTopicsOf(packagename, regid)

    '''
    获取失效的regId列表不需要传递任何HTTP参数。
    获取失效的regId列表，每次请求最多返回1000个regId。
    每次请求之后，成功返回的失效的regId将会从MiPush数据库删除。
    存在失效的regid
        {“result”:”ok”,”description”:”成功”,”data”:{“list”:["regid1","regid2","regid3"]},”code”:0}
    不存在失效的regid
        {“result”:”ok”,”description”:”成功”,”data”:{“list”:[]},”code”:0}
    '''
    client.getInvalidRegIds()

    ###### Sender #####

    '''指定regId列表群发'''
    client.sendToId(message, regid_list)

    '''指定别名列表群发'''
    client.sendToAlias(message, alias_list)

    '''指定userAccount列表群发'''
    client.sendToUserAccount(message, account_list)

    '''指定topic群发'''
    client.broadcastTopic(message, topic)

    '''广播消息，多个topic，支持topic间的交集、并集或差集'''
    client.broadcastTopicList(message, topic_list, topic_op)

    '''向所有设备发送消息'''
    client.broadcastAll(message)

    '''多条发送'''
    client.multiSend(targetMessage_list, ty, timeToSend=None)

    '''检测定时任务是否存在'''
    client.checkScheduleJobExist(msgid)

    '''删除定时任务'''
    client.deleteScheduleJob(msgid)

    ##### Stats #####

    ''' 获取消息的统计数据 '''
    client.getStats(packagename, startDate, endDate)

    ##### Subscription #####

    ''' 订阅RegId的标签 '''
    client.subscribeForRegid(regid_list, topic, packagename=None)

    ''' 取消订阅RegId的标签 '''
    client.unsubscribeForRegid(regid_list, topic, packagename=None)

    ''' 订阅Alias的标签 '''
    client.subscribeForAlias(alias_list, topic, packagename=None)

    ''' 取消订阅Alias的标签 '''
    client.unsubscribeForAlias(alias_list, topic, packagename=None)

    ##### Trace #####

    ''' 通过Id追踪消息状态 '''
    client.getMessageStatusById(msgid)

    ''' 通过JobKey追踪消息状态 '''
    client.getMessageStatusByJobKey(jobkey)

    ''' 通过时间范围追踪消息状态 '''
    client.getMessagesStatusByTimeArea(beginTime, endTime)
