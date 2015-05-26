# -*- coding: utf-8 -*-
from __future__ import unicode_literals
 
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
 
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk.messages import *

from wechat_sdk.context.framework.django import DatabaseContextStore
 
WECHAT_TOKEN = '123456'
AppID = 'wxdddaafdc0183cfa7'
AppSecret = '6902741c3bb16f1ce177ba4c41eba391'
 
# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)


@csrf_exempt
def index(request):

    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
 
        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')
 
        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")
 
 
    # 解析本次请求的 XML 数据
    print(request.body)
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')


    # 获取解析好的微信请求信息

    article=[
        {
            'title':'JiesongSitansong',
            'description': '图文内容',
            'picurl': 'http://b74.photo.store.qq.com/psu?/127abb2c-86b7-4e56-8943-46a5ebcf01a4/ROWX*yOc*MQ4IEoESFAttyUreW2dgcQ5BNJ4AvxVDno!/b/Yf63Jyy9HgAAYqseICxSDgAA&bo=3wHgAQAAAAABBBw!&rf=viewer_4',
            'url': 'http://baike.baidu.com/link?url=vucC-dzLTWjdmxrlFbq-fKzFGEDuqhL0869GyzxPjocmvKZSgun7Wmw5zpQB2SHuKm8hby8wIv27ZyNmRbox5w8wf4_EiEQDtkxtwwKif4HNzfoVVHxGA5Y-8lpFRUbN0Pbl1hd3E4KcZpDCjrQING_KrmM7wqbXxzM_YFRCelplNr9UZR4dR_O_OUtgZgfO',
        },
        {
            'title':'HEHE',
            'description': '图文内容',
            'picurl': 'http://b186.photo.store.qq.com/psb?/127abb2c-86b7-4e56-8943-46a5ebcf01a4/yhZxua*tH9jd.M6NUg7SFVJ6bhnk6w84iHUODHqekRE!/b/dPIO4m59FwAA&bo=xgBnAAAAAAAFAII!&rf=viewer_4',
            'url': 'http://baozoumanhua.com/',
        },
          {
            'title':'HEiHEi',
            'description': '图文内容',
            'picurl': 'http://b276.photo.store.qq.com/psb?/127abb2c-86b7-4e56-8943-46a5ebcf01a4/Yo4yMsaRDkvyqPFd8D4ffHTLvl6oqoYuAkmXowKX9LM!/b/dD4AjaSZHwAA&bo=ZABkAAAAAAACUHQ!&rf=viewer_4',
            'url': 'http://baozoumanhua.com/',
        },

    ]
    message = wechat_instance.get_message()
    context = DatabaseContextStore(openid=message.source)

    '''followers= wechat_instance.get_followers()
    users=followers.get('data')
    for v in users.values():
        for user in v:
            wechat_instance.send_article_message(user,articles=article)'''
    # 关注事件以及不匹配时的默认回复
    #print(wechat_instance.show_qrcode(ticket='gQEq8DoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL2NVeEdYY3ZsTDFkV0ZpcVY2bUI0AAIESZFZVQMEAAAAAA=='))
    response = wechat_instance.response_text(
        content = (
            '感谢您的关注！\n回复【功能】两个字查看支持的功能，还可以回复任意内容开始聊天'
            '\n【<a href="http://guandashi.xicp.net/polls">Welcom to mysite 1</a>】'
            ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        step = context.get('step', 1)  # 从上下文对话数据中取出 'step' 所对应的内容(当前对话次数)，如果没有则返回 1
        last_text = context.get('last_text')  # 从上下文对话数据中取出 'last_text' 所对应的内容(上次对话内容)
        # 生成字符串
        now_text = u'这是第 %d 次对话' % step
        if step > 1:
            now_text += u'，上一次对话文字：%s' % last_text
        # 将新的数据存入上下文对话中
        context['step'] = step + 1
        context['last_text'] = message.content
        response = wechat_instance.response_text(content=now_text)


    elif isinstance(message, EventMessage):
        reply_text2=message.key
        if(reply_text2=='GIVE_A_MUSIC'):
            response = wechat_instance.response_voice(media_id='2kVVbW1swvpK5JP3LJlJDudu4rGnD_vUqpxzDYT4ei4TKmaTyyNKjHkNwogehn8w')
        elif(reply_text2=='Contact_Us'):
            
            response = wechat_instance.response_news(article)

        elif(reply_text2=='GIVE_A_GOOD'):
            response = wechat_instance.response_music(music_url='http://guandashi.xicp.net/static/AreYouOk.mp3',title='Are You OK',description='artist is leijun')
        eventtype=message.type
        if(eventtype=='subscribe'):
            response = wechat_instance.response_text(content='感谢您的关注')

    elif isinstance(message,LocationMessage):
        locat=message.location
        response = wechat_instance.response_text(content=locat)
    elif isinstance(message, ImageMessage):
        #response = wechat_instance.response_text(content='tu pian di zhi:'+message.picurl)
        #response = wechat_instance.response_image(media_id='vc_XuaG6MTqc7tI95GZa1e9Nc5K8T8xQDBzPGyr9ONG1rLlECD4Yc6waOYwI9x5q')
        response = wechat_instance.download_media(message.media_id)
        with open('downpic.jpg', 'wb') as fd:
            for chunk in response.iter_content(1024):
                fd.write(chunk)
        response = wechat_instance.response_text(content='tu pian yi jing bei xia zai')
    elif isinstance(message,VideoMessage):
        media_id=message.media_id
        response = wechat_instance.response_text(content='fang wen mei ti de ID :'+media_id)
    elif isinstance(message, UnknownMessage):
        response = wechat_instance.response_text(content='unknownmessage')
    context.save()
    return HttpResponse(response, content_type="application/xml")
