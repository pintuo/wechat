# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk.messages import *
from .models import *
from wechat_sdk.context.framework.django import DatabaseContextStore
from netbar.checkcard import *

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
    message = wechat_instance.get_message()
    # 关注事件以及不匹配时的默认回复
    #print(wechat_instance.show_qrcode(ticket='gQEq8DoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xL2NVeEdYY3ZsTDFkV0ZpcVY2bUI0AAIESZFZVQMEAAAAAA=='))
    response = wechat_instance.response_text(
        content = (
            '感谢您的关注！\n回复【功能】两个字查看支持的功能.'
            '\n【<a href="http://guandashi.xicp.net/polls">Welcom to mysite 1</a>】'
            ))
    if isinstance(message, TextMessage):
        # 当前会话内容
        content = message.content.upper()
        content=content.strip()
        if(content.startswith('BD',0,2)==True):
            card=content[2:]
            ermsg=checkIdcard(card)
            user=User.objects.filter(openid=message.source)
            if(ermsg.decode("utf-8")==u'验证通过!' and len(user)==0 ):
                u=wechat_instance.get_user_info(message.source)
                newuser=User(openid=message.source,cardno=card,name=u['nickname'],sex=u['sex'])
                newuser.save()
                response = wechat_instance.response_text(content='成功绑定VIP')
            elif(ermsg.decode("utf-8")==u'验证通过!' and len(user)!=0 ):
                response = wechat_instance.response_text(content='您已经绑定了VIP，无需重新绑定\n（注意：一个微信号只能绑定一个身份证号码）。')
            else:
                response = wechat_instance.response_text(content=ermsg)
        #response = wechat_instance.response_text(content='hhh')
        elif(content=='功能'):
            response = wechat_instance.response_text(content='回复“BD”+身份证号码，可以绑定VIP，\n还可以进入菜单查询网吧剩余机器，\n买吃买喝，呼叫网管等。')


    elif isinstance(message, EventMessage):
        reply_text2=message.key
        '''if(reply_text2=='RemainPC'):
            response = wechat_instance.response_text(content='剩余 '+str(pcset.__len__())+' 台主机, 主机号分别是: '+pcid)'''
        if(reply_text2=='BindVIP'):
            response = wechat_instance.response_text('请输入“BD”+身份证号码。\n例如：bd321326199509026644\n（注意：一个微信号只能绑定一个身份证号码）')

        elif(reply_text2=='ReservePC'):
             #selsql='select numb num from Comuter where usable =%s'
            pcset=Computer.objects.filter(usable='0')
            pcid=''
            for pc in pcset:
                pcid+=pc.numb+','
            response = wechat_instance.response_music(music_url='http://guandashi.xicp.net/static/AreYouOk.mp3',title='Are You OK',description='歌手：雷军')
        elif(reply_text2=='CallMaster'):

            response = wechat_instance.response_text(content='消息已传达网管，五分钟内为您服务。')
        elif(reply_text2=='ConsumeQuery'):
            response = wechat_instance.response_text(content='该功能暂未开通。')

    elif isinstance(message,LocationMessage):
        locat=message.location
        response = wechat_instance.response_text(content='您所在地理位置经纬度分别是：'+locat)
    elif isinstance(message, ImageMessage):
        response = wechat_instance.response_image(media_id=message.media_id)
    elif isinstance(message,VideoMessage):
        media_id=message.media_id
        response = wechat_instance.response_text(content='该视频地址是： :'+message.thumb_media_id)
    elif isinstance(message, UnknownMessage):
        response = wechat_instance.response_text(content='不支持的消息类型')

    return HttpResponse(response, content_type="application/xml")
