# -*- coding: utf-8 -*-
# import urllib


class Message(object):

    def __init__(self):
        self._data = {}
        self._data['notify_id'] = 0
        self._data['notify_type'] = -1
        self._data['payload'] = ''

    def build(self, packagename, title, description, payload=None,
              pass_through=0, notify_type=-1, notify_id=0,
              time_to_live=None, time_to_send=None, extra=None):
        '''
        restricted_package_name  # 支持多包名
        payload  # payload是字符串
        title  # 在通知栏的标题，长度小于16
        description  # 在通知栏的描述，长度小于128
        pass_through  # 是否透传给app(1 透传 0 通知栏信息)
        notify_type  可以是DEFAULT_ALL或者以下其他几种的OR组合
            DEFAULT_ALL = -1;
            DEFAULT_SOUND  = 1;  // 使用默认提示音提示；
            DEFAULT_VIBRATE = 2;  // 使用默认震动提示；
            DEFAULT_LIGHTS = 4;   // 使用默认led灯光提示；
        notify_id  # 0-4同一个notifyId在通知栏只会保留一条
        time_to_live  # 可选项,long,当用户离线是，消息保留时间，默认两周，单位ms
        time_to_send  # 可选项,long,定时发送消息，用自1970年1月1日以来00:00:00.0 UTC时间表示（以毫秒为单位的时间）。
        extra  # 可选项，额外定义一些key value（字符不能超过1024，key不能超过10个）
        extra的一部分可选项:(不包括全部,更多查看文档)
            *locale  可以接收消息的设备的语言范围，用逗号分隔。
            *locale_not_in
            *model  model支持三种用法:机型、品牌、价格区间
            *model_not_in
            *app_version  可以接收消息的app版本号，用逗号分割。
            *app_version_not_in
            *connpt  指定在特定的网络环境下才能接收到消息;目前只支持指定wifi;
            *jobkey  设置消息的组ID
            *ticker  开启通知消息在状态栏滚动显示
            *sound_uri  自定义通知栏消息铃声
            *notify_foreground  预定义通知栏消息的点击行为,参考文档2.2.3
            *flow_control  控制是否需要进行平缓发送，1表示平缓，0否
            *notify_effect  指定点击行为
        '''

        if not isinstance(packagename, (list, tuple, set)):
            packagename = [packagename]
        self._data['restricted_package_name'] = ','.join(packagename)
        self._data['title'] = title
        self._data['description'] = description
        self._data['pass_through'] = pass_through
        self._data['notify_type'] = notify_type
        self._data['notify_id'] = notify_id
        if payload:
            self._data['payload'] = payload
        if time_to_live is not None:
            self._data['time_to_live'] = time_to_live
        if time_to_send is not None:
            self._data['time_to_send'] = time_to_send
        self.fields = {}
        self.json_infos = {}

        for k, v in self._data.iteritems():
            self.fields[k] = v
            self.json_infos[k] = v

        EXTRA_PREFIX = 'extra.'
        self.json_infos['extra'] = {}
        for k, v in (extra or {}).iteritems():
            self.fields[EXTRA_PREFIX + k] = v
            self.json_infos['extra'][k] = v

    def get_fields(self):
        return self.fields

    def getJSONInfos(self):
        return self.json_infos
