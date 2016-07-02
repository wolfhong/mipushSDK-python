# -*- coding: utf-8 -*-

'''
 * 常量定义.
 * @author wolfhong
 * @name Constants
 * @desc 常量定义
 *
'''


class Constants(object):

    reg_url = '/v3/message/regid'
    alias_url = '/v3/message/alias'
    user_account_url = '/v2/message/user_account'
    topic_url = '/v3/message/topic'
    multi_topic_url = '/v3/message/multi_topic'
    all_url = '/v3/message/all'
    multi_messages_regids_url = '/v2/multi_messages/regids'
    multi_messages_aliases_url = '/v2/multi_messages/aliases'
    multi_messages_user_accounts_url = '/v2/multi_messages/user_accounts'
    stats_url = '/v1/stats/message/counters'
    message_trace_url = '/v1/trace/message/status'
    messages_trace_url = '/v1/trace/messages/status'
    validation_regids_url = '/v1/validation/regids'
    subscribe_url = '/v2/topic/subscribe'
    unsubscribe_url = '/v2/topic/unsubscribe'
    subscribe_alias_url = '/v2/topic/subscribe/alias'
    unsubscribe_alias_url = '/v2/topic/unsubscribe/alias'
    delete_schedule_job = '/v2/schedule_job/delete'
    check_schedule_job_exist = '/v2/schedule_job/exist'
    get_all_aliases = '/v1/alias/all'
    get_all_topics = '/v1/topic/all'

    fetch_invalid_regids_url = 'https://feedback.xmpush.xiaomi.com/v1/feedback/fetch_invalid_regids'

    UNION = 'UNION'  # 并集
    INTERSECTION = 'INTERSECTION'  # 交集
    EXCEPT = 'EXCEPT'  # 差集
