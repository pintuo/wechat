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
#from django.shortcuts import get_object_or_404, render

WECHAT_TOKEN = '123456'
AppID = 'wxdddaafdc0183cfa7'
AppSecret = '6902741c3bb16f1ce177ba4c41eba391'

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)
wechat_instance.create_menu({
        "button": [
            {
                "name": "来上网吧",
                "sub_button": [
                     {
                        "type": "click",
                        "name": "绑定VIP",
                        "key": "BindVIP",
                    },
		            {
                        "type": "view",
                        "name": "预定机器",
                        "url": "http://guandashi.xicp.net/netbar_reservePC",
                    },
                    {
                        "type": "click",
                        "name": "优惠活动",
                        "key": "Promotio",
                    },

                ]
            },
            {
                "type": "view",
                "name": "吃与喝",
                "url": "http://guandashi.xicp.net/eleme",
            },
            {
                "name": "服务中心",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "呼叫网管",
                        "key": "CallMaster",
                    },
                    {
                        "type": "click",
                        "name": "消费查询",
                        "key": "ConsumeQuery",
                    },
                   {
                        "type": "click",
                        "name": "结账下机",
                        "key": "CheckOut",
                    },
                ]
            }
        ]
    })
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
    article=[
                {
                    'title':'博达网咖--年轻人的竞技场',
                    'description': '图文内容',
                    'picurl': 'http://pic26.nipic.com/20121220/11562079_220947605169_2.jpg',
                    'url': '',
                },
                {
                    'title':'回复“功能”获取服务口令',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a1.jpg',
                    'url': 'http://guandashi.xicp.net/static/a1.jpg',
                },
                  {
                    'title':'回复“活动”获取优惠信息',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a2.jpg',
                    'url': 'http://guandashi.xicp.net/static/a2.jpg',
                },
                {
                    'title':'点击“吃与喝”菜单享受美味',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/chikencoke.jpg',
                    'url': 'http://guandashi.xicp.net/static/chikencoke.jpg',
                },
            ]
    Promotio=[
                {
                    'title':'早市1元',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a4.jpg',
                    'url': 'http://guandashi.xicp.net/static/a4.jpg',
                },
                {
                    'title':'充值好礼',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a5.jpg',
                    'url': 'http://guandashi.xicp.net/static/a5.jpg',
                },
                  {
                    'title':'英雄联盟等你来战',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a6.jpg',
                    'url': 'http://guandashi.xicp.net/static/a6.jpg',
                },
                {
                    'title':'积分转盘',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a2.jpg',
                    'url': 'http://guandashi.xicp.net/lottery',
                },
            ]
    response = wechat_instance.response_news(article)

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
        elif(content=='活动'):
            #response = wechat_instance.response_text(content='博达网咖开业充值送好礼\n充100元得120元\n充200元得250元\n网费多充多送\n详情见店堂公告')
            article=[
                {
                    'title':'早市1元',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a4.jpg',
                    'url': 'http://guandashi.xicp.net/static/a4.jpg',
                },
                {
                    'title':'充值好礼',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a5.jpg',
                    'url': 'http://guandashi.xicp.net/static/a5.jpg',
                },
                  {
                    'title':'英雄联盟等你来战',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a6.jpg',
                    'url': 'http://guandashi.xicp.net/static/a6.jpg',
                },
                {
                    'title':'积分转盘',
                    'description': '图文内容',
                    'picurl': 'http://guandashi.xicp.net/static/a2.jpg',
                    'url': 'http://guandashi.xicp.net/lottery',
                },
            ]
            response = wechat_instance.response_news(article)
        elif(content=='推送' and message.source=='ovIfQtzWVePVLotiPmCOgCpXJbzA'):
            followers= wechat_instance.get_followers()
            users=followers.get('data')
            response = wechat_instance.response_text(content='推送完成')
            # wechat_instance.send_text_message(user_id='ovIfQtyugGh1uMnLqhAlx92J1U08',content='article')
            for v in users.values():
                for user in v:
                    print(user)
                    wechat_instance.send_article_message(user_id=user,articles=Promotio)
    elif isinstance(message, EventMessage):
        reply_text2=message.key
        if(reply_text2=='BindVIP'):
            response = wechat_instance.response_text('请输入“BD”+身份证号码。例如：\nbd321326199509026644\n（注意：一个微信号只能绑定一个身份证号码）')
        elif(reply_text2=='EatDrink'):
            article=[
                {
                    'title':'芝士蛋糕(30元)',
                    'description': '图文内容',
                    'picurl': 'http://pic1a.nipic.com/2008-12-01/200812192058760_2.jpg',
                    'url': 'http://www.nipic.com/show/1/56/b009ab3bdb9ff4ef.html',
                },
                {
                    'title':'油炸鸡翅(15元)',
                    'description': '图文内容',
                    'picurl': 'http://img4.imgtn.bdimg.com/it/u=1146571026,3505256192&fm=21&gp=0.jpg',
                    'url': 'http://www.nipic.com/show/1/55/6533779k90cefe6e.html',
                },
                  {
                    'title':'饺子(6元一两)',
                    'description': '图文内容',
                    'picurl': 'http://img1.imgtn.bdimg.com/it/u=1124969323,215308632&fm=21&gp=0.jpg',
                    'url': 'http://baozoumanhua.com/',
                },
                {
                    'title':'可乐(2元)',
                    'description': '图文内容',
                    'picurl': 'http://www.justsayno.com/wp-content/uploads/2014/10/coke.jpg',
                    'url': 'http://baozoumanhua.com/',
                },
            ]
            response = wechat_instance.response_news(article)
        elif(reply_text2=='CallMaster'):
            response = wechat_instance.response_text(content='消息已传达网管，五分钟内为您服务。')
        elif(reply_text2=='ConsumeQuery'):
            response = wechat_instance.response_text(content='该功能暂未开通。')
        elif(reply_text2=='CheckOut'):
            response = wechat_instance.response_text(content='该功能暂未开通。')
        elif(reply_text2=='Promotio'):
            response = wechat_instance.response_news(Promotio)
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

def reservePC(request):
    pcset=Computer.objects.filter(usable='0')
    print(pcset)
    return render(request, 'netbar/reserve.html', {'pcset': pcset})

def product(request):
    return render(request, 'netbar/product.html')
def single(request):
    return render(request, 'netbar/single.html')
def eleme(request):
    return render(request, 'netbar/eleme.html')
def lottery(request):
    return render(request, 'netbar/lottery.html')
def login(request):
    return render(request, 'netbar/login.html')