from wechat_sdk import WechatBasic


token = 'WECHAT_TOKEN' 
signature = 'f24649c76c3f3d81b23c033da95a7a30cb7629cc' 
timestamp = '1406799650' 
nonce = '1505845280'  


body_text = """
<xml>
<ToUserName><![CDATA[touser]]></ToUserName>
<FromUserName><![CDATA[fromuser]]></FromUserName>
<CreateTime>1405994593</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<Content><![CDATA[hehe]]></Content>
<MsgId>6038700799783131222</MsgId>
</xml>
"""

wechat = WechatBasic(token=token)

if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
   
    wechat.parse_data(body_text)

    message = wechat.get_message()
   

    response = None
    if message.type == 'text':
        if message.content == 'wechat':
            response = wechat.response_text(u'^_^')
        else:
            response = wechat.response_text(u'wenzi')
    elif message.type == 'image':
        response = wechat.response_text(u'tupian')
    else:
        response = wechat.response_text(u'weizhi')
	#print message.type()
   # print message.content

    print response
