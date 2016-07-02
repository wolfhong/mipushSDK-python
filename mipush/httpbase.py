# -*- coding: utf-8 -*-
import json
import requests
# import traceback
from .constants import Constants

SuccessCode = 0


class MipushError(Exception):

    def __init__(self, result):
        self.status_code = result.status_code
        self.raw = result.raw


class Result(object):

    def __init__(self, req):
        self.status_code = req.status_code
        try:
            raw = json.loads(req.text)
            self.raw = raw
            self.errorCode = raw['code']
        except Exception:
            self.raw = req.text
            raise MipushError(self)


class MipushClient(object):

    def __init__(self, version, appsecret, retries=1, timeout=3):
        '''
        @params version 发布版本或者测试版本:release dev
        @params appsecret 注册后申请取得
        @params retries 因网络异常允许的重试次数,默认重试一次
        @params timeout 接口的请求超时时间,默认3秒
        '''
        self.appsecret = appsecret
        self.retries = retries
        self.timeout = timeout

        assert version in ['release', 'dev']
        if version == 'release':
            self.domain = 'https://api.xmpush.xiaomi.com'
        else:
            self.domain = 'https://sandbox.xmpush.xiaomi.com'

    def getResult(self, method, url, fields):
        '''发送请求，获取result，带重试'''
        r = self._getReq(method, url, fields)
        result = Result(r)
        if result.errorCode == SuccessCode:
            return result
        # 重试
        retries = self.retries
        while retries > 0:
            retries -= 1
            r = self._getReq(method, url, fields)
            result = Result(r)
            if result.errorCode == SuccessCode:
                return result
        raise MipushError(result)

    def _getReq(self, method, url, fields):
        '''发送请求'''
        headers = {
            'Authorization': 'key=%s' % self.appsecret,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        assert method in ['post', 'get']
        timeout = self.timeout
        if method == 'get':
            r = requests.get(url, params=fields, headers=headers, timeout=timeout)
        elif method == 'post':
            r = requests.post(url, params=fields, headers=headers, timeout=timeout)
        return r

    # ##### DevTools #####

    def getAliasesOf(self, packagename, regid):
        ''' 获取一个应用的某个用户目前设置的所有Alias '''
        url = self.domain + Constants.get_all_aliases
        fields = {'registration_id': regid, 'restricted_package_name': packagename}
        return self.getResult('get', url, fields)

    def getTopicsOf(self, packagename, regid):
        ''' 获取一个应用的某个用户目前订阅的所有Topic '''
        url = self.domain + Constants.get_all_topics
        fields = {'registration_id': regid, 'restricted_package_name': packagename}
        return self.getResult('get', url, fields)

    def getInvalidRegIds(self):
        '''
        获取失效的regId列表不需要传递任何HTTP参数。
        获取失效的regId列表，每次请求最多返回1000个regId。
        每次请求之后，成功返回的失效的regId将会从MiPush数据库删除。
        存在失效的regid
            {“result”:”ok”,”description”:”成功”,”data”:{“list”:["regid1","regid2","regid3"]},”code”:0}
        不存在失效的regid
            {“result”:”ok”,”description”:”成功”,”data”:{“list”:[]},”code”:0}
        '''
        url = Constants.fetch_invalid_regids_url
        fields = {}
        return self.getResult('get', url, fields)

    # ##### Sender #####

    def sendToId(self, message, regid_list):
        '''指定regId列表群发'''
        if not isinstance(regid_list, (list, tuple, set)):
            regid_list = [regid_list, ]  # 一个元素的list

        url = self.domain + Constants.reg_url
        fields = message.get_fields()
        fields['registration_id'] = ','.join([k for k in regid_list if k])
        return self.getResult('post', url, fields)

    def sendToAlias(self, message, alias_list):
        '''指定别名列表群发'''
        if not isinstance(alias_list, (list, tuple, set)):
            alias_list = [alias_list]

        url = self.domain + Constants.alias_url
        fields = message.get_fields()
        fields['alias'] = ','.join([k for k in alias_list if k])
        return self.getResult('post', url, fields)

    def sendToUserAccount(self, message, account_list):
        '''指定userAccount列表群发'''
        if not isinstance(account_list, (list, tuple, set)):
            account_list = [account_list]

        url = self.domain + Constants.user_account_url
        fields = message.get_fields()
        fields['user_account'] = ','.join([k for k in account_list if k])
        return self.getResult('post', url, fields)

    def broadcastTopic(self, message, topic):
        '''指定topic群发'''
        url = self.domain + Constants.topic_url
        fields = message.get_fields()
        fields['topic'] = topic
        return self.getResult('post', url, fields)

    def broadcastTopicList(self, message, topic_list, topic_op):
        '''广播消息，多个topic，支持topic间的交集、并集或差集'''
        if len(topic_list) == 1:
            return self.broadcastTopic(message, topic_list)
        url = self.domain + Constants.multi_topic_url
        fields = message.get_fields()
        fields['topics'] = u';$;'.join([k for k in topic_list if k])
        fields['topic_op'] = topic_op
        return self.getResult('post', url, fields)

    def broadcastAll(self, message):
        '''向所有设备发送消息'''
        url = self.domain + Constants.all_url
        fields = message.get_fields()
        return self.getResult('post', url, fields)

    def multiSend(self, targetMessage_list, ty, timeToSend=None):
        '''多条发送'''
        TARGET_TYPE_REGID = 1
        TARGET_TYPE_ALIAS = 2
        TARGET_TYPE_USER_ACCOUNT = 3
        url = {
            TARGET_TYPE_REGID: self.domain + Constants.multi_messages_regids_url,
            TARGET_TYPE_ALIAS: self.domain + Constants.multi_messages_aliases_url,
            TARGET_TYPE_USER_ACCOUNT: self.domain + Constants.multi_messages_user_accounts_url,
        }[ty]
        data_list = [t.get_fields() for t in targetMessage_list]
        fields = {}
        fields['messages'] = json.dumps(data_list)
        if timeToSend:
            fields['time_to_send'] = timeToSend
        return self.getResult('post', url, fields)

    def checkScheduleJobExist(self, msgid):
        '''检测定时任务是否存在'''
        url = self.domain + Constants.check_schedule_job_exist
        fields = {'job_id': msgid}
        return self.getResult('post', url, fields)

    def deleteScheduleJob(self, msgid):
        '''删除定时任务'''
        url = self.domain + Constants.delete_schedule_job
        fields = {'job_id': msgid}
        return self.getResult('post', url, fields)

    # #### Stats #####

    def getStats(self, packagename, startDate, endDate):
        '''
        @brief 获取消息的统计数据
        @params packagename IOS设备,传入App的Bundle Id;Android设备,传入App的包名
        @params startDate 表示开始日期,如20140214
        @params endDate 表示结束日期,如20140314
        '''
        url = self.domain + Constants.stats_url
        fields = {
            'start_date': startDate,
            'end_date': endDate,
            'restricted_package_name': packagename,
        }
        return self.getResult('get', url, fields)

    # #### Subscription #####

    def subscribeForRegid(self, regid_list, topic, packagename=None):
        ''' 订阅RegId的标签 '''
        if not isinstance(regid_list, (list, tuple, set)):
            regid_list = [regid_list]

        url = self.domain + Constants.subscribe_url
        fields = {'topic': topic}
        fields['registration_id'] = ','.join([k for k in regid_list if k])
        if packagename:
            fields['restricted_package_name'] = packagename
        return self.getResult('post', url, fields)

    def unsubscribeForRegid(self, regid_list, topic, packagename=None):
        ''' 取消订阅RegId的标签 '''
        if not isinstance(regid_list, (list, tuple, set)):
            regid_list = [regid_list]

        url = self.domain + Constants.unsubscribe_url
        fields = {'topic': topic}
        fields['registration_id'] = ','.join([k for k in regid_list if k])
        if packagename:
            fields['restricted_package_name'] = packagename
        return self.getResult('post', url, fields)

    def subscribeForAlias(self, alias_list, topic, packagename=None):
        ''' 订阅Alias的标签 '''
        if not isinstance(alias_list, (list, tuple, set)):
            alias_list = [alias_list]

        url = self.domain + Constants.subscribe_alias_url
        fields = {'topic': topic}
        fields['aliases'] = ','.join([k for k in alias_list if k])
        if packagename:
            fields['restricted_package_name'] = packagename
        return self.getResult('post', url, fields)

    def unsubscribeForAlias(self, alias_list, topic, packagename=None):
        ''' 取消订阅Alias的标签 '''
        if not isinstance(alias_list, (list, tuple, set)):
            alias_list = [alias_list]

        url = self.domain + Constants.unsubscribe_alias_url
        fields = {'topic': topic}
        fields['aliases'] = ','.join([k for k in alias_list if k])
        if packagename:
            fields['restricted_package_name'] = packagename
        return self.getResult('post', url, fields)

    # #### Trace #####

    def getMessageStatusById(self, msgid):
        '''
        @brief 通过Id追踪消息状态
        @params msgid 发送消息时返回的msgid
        '''
        url = self.domain + Constants.message_trace_url
        fields = {'msg_id': msgid}
        return self.getResult('get', url, fields)

    def getMessageStatusByJobKey(self, jobkey):
        '''
        @brief 通过JobKey追踪消息状态
        @params jobKey 发送消息时设置的jobKey
        '''
        url = self.domain + Constants.message_trace_url
        url = self.domain + Constants.message_trace_url
        fields = {'job_key': jobkey}
        return self.getResult('get', url, fields)

    def getMessagesStatusByTimeArea(self, beginTime, endTime):
        '''
        @brief 通过时间范围追踪消息状态
        @params beginTime 表示开始时间戳，单位ms
        @params endTime 表示结束时间戳，单位ms
        '''
        url = self.domain + Constants.message_trace_url
        fields = {'begin_time': beginTime, 'end_time': endTime}
        return self.getResult('get', url, fields)
