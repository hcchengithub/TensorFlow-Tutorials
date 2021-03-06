import itchat
from itchat.content import * # TEXT PICTURE 等 constant 的定義
import peforth
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import time
# OK time :> ctime() . cr
# Tue Dec 12 14:34:11 2017
import random

# Anti-Robot delay time , thanks to Rainy's great idea.
nextDelay = random.choice(range(3,18)) 

import inception
inception.maybe_download()
model = inception.Inception() # The Inception v3 model 

# Inhibit 'bye' command, it terminates DOSBox session immediately 
# and leaves 'bye' in msg! Only a re-login can resolve it. To avoid this,
# decorator must return instead of doing the 'bye' command directly.
peforth.ok(loc=locals(),cmd=":> [0] constant locals : bye locals :> ['itchat'].logout() ; exit")  

# Send message to friend or chatroom depends on the given 'send'
# function. It can be itchat.send or msg.user.send up to the caller.
# WeChat text message has a limit at about 2000 utf-8 characters so
# we need to split a bigger string into chunks.
def send_chunk(text, send, pcs=2000):
    s = text
    while True:
        if len(s)>pcs:
            print(s[:pcs]); send(s[:pcs])
        else:
            print(s); send(s)
            break
        s = s[pcs:]    

# Console is a peforth robot that listens and talks.
# Used in chatting with friends and in a chatroom.
def console(msg,cmd):
    if cmd:
        print(cmd)  # already on the remote side, don't need to echo 
        # re-direct the display to peforth screen-buffer
        peforth.vm.dictate("display-off")  
        try:
            peforth.vm.dictate(cmd)
        except Exception as err:
            errmsg = "Failed! : {}".format(err)
            peforth.vm.dictate("display-on")
            send_chunk(errmsg, msg.user.send)
        else:
            peforth.vm.dictate("display-on screen-buffer")
            screen = peforth.vm.pop()[0]
            send_chunk(screen, msg.user.send)
        send_chunk("OK", msg.user.send)


#        
# 讓 Inception V3 看照片，回答那啥。        
#        
def predict(msg):
    results = time.ctime() + '\n'
    results += 'Google Inception V3 thinks it is:\n'
    msg.download('download\\' + msg.fileName)  # 照片放在 working directory/download 下
    if msg.fileName.strip().lower().endswith((".jpeg",'.jpg','.png')):
        pred = model.classify(image_path=('download\\'+ msg.fileName).strip())
        results += model.print_scores(pred=pred,k=10,only_first_name=True)
    else:
        results += 'Ooops! jpeg pictures only, please. {} is not one.\n'.format(msg.fileName)
    return results
        
#
# 不要干擾借用帳號的同仁，只在特定的 ChatRoom 裡工作。
#
# @itchat.msg_register(TEXT)
# def _(msg):
#     if peforth.vm.debug==99: peforth.ok('99> ',loc=locals(),cmd=":> [0] inport cr")  # breakpoint    
#     console(msg, msg.Text.strip())
# 
# @itchat.msg_register([MAP, CARD, NOTE, SHARING])
# def _(msg):
#     if peforth.vm.debug==11: peforth.ok('11> ',loc=locals(),cmd=":> [0] inport cr")  # breakpoint    
#     send_chunk('%s: %s' % (msg.type, msg.text), msg.user.send)
# 
# @itchat.msg_register(PICTURE)
# def _(msg):
#     if peforth.vm.debug==2211: peforth.ok('2211> ',loc=locals(),cmd=":> [0] constant loc2211 cr")  # breakpoint    
#     # msg.download(msg.fileName)  # 放在 working directory 下
#     # pred = model.classify(image_path=msg.fileName.strip())
#     # results = model.print_scores(pred=pred,k=10,only_first_name=True)
#     return predict(msg)
    
# @itchat.msg_register([RECORDING, ATTACHMENT, VIDEO])
# def _(msg):
#     if peforth.vm.debug==22: peforth.ok('22> ',loc=locals(),cmd=":> [0] inport cr")  # breakpoint    
#     msg.download(msg.fileName)
#     typeSymbol = {
#         PICTURE: 'img',
#         VIDEO: 'vid', }.get(msg.type, 'fil')
#     return '@%s@%s' % (typeSymbol, msg.fileName)
#
# @itchat.msg_register(FRIENDS)
# def _(msg):
#     if peforth.vm.debug==33: peforth.ok('33> ',loc=locals(),cmd=":> [0] inport cr")  # breakpoint    
#     msg.user.verify()
#     send_chunk('Nice to meet you!', msg.user.send)

@itchat.msg_register(ATTACHMENT, isGroupChat=True)
def _(msg):
    global nextDelay
    time.sleep(nextDelay)  # Anti-Robot delay 
    nextDelay = random.choice(range(3,18))
    if peforth.vm.debug==55: peforth.ok('55> ',loc=locals(),cmd=":> [0] constant loc55 cr")  # breakpoint    
    if msg.user.NickName[:5]=='AILAB': # 只在 AILAB 工作，過濾掉其他的。
        msg.download('download\\' + msg.fileName)
        send_chunk('Attachment: %s received at %s' % (msg.fileName,time.ctime()), msg.user.send)
        send_chunk('Next anti-robot delay time: %i seconds' % (nextDelay), msg.user.send)

@itchat.msg_register(TEXT, isGroupChat=True)
def _(msg):
    global nextDelay
    time.sleep(nextDelay)  # Anti-Robot delay 
    nextDelay = random.choice(range(3,18))
    if peforth.vm.debug==44: peforth.ok('44> ',loc=locals(),cmd=":> [0] constant loc44 cr")  # breakpoint    
    if msg.user.NickName[:5]=='AILAB': # 只在 AILAB 工作，過濾掉其他的。
        if msg.isAt: 
            cmd = msg.text.split(maxsplit=1)[1] # remove the leading @nickName
            console(msg, cmd)
            send_chunk('Next anti-robot delay time: %i seconds' % (nextDelay), msg.user.send)

@itchat.msg_register(PICTURE, isGroupChat=True)
def _(msg):
    global nextDelay
    time.sleep(nextDelay)  # Anti-Robot delay 
    nextDelay = random.choice(range(3,18))
    if peforth.vm.debug==4411: peforth.ok('4411> ',loc=locals(),cmd=":> [0] constant loc4411 cr")  # breakpoint    
    if msg.user.NickName[:5]=='AILAB': # 只在 AILAB 工作，過濾掉其他的。
        send_chunk(predict(msg), msg.user.send)
        send_chunk('Next anti-robot delay time: %i seconds' % (nextDelay), msg.user.send)
    
itchat.auto_login(hotReload=False)
itchat.run(debug=False, blockThread=True)
peforth.ok('Examine> ',loc=locals(),cmd=':> [0] value locals')

# Bug list
# [ ] 正常對話不需 delay 
# [ ] "Next anti-robot delay time" 往上合併好再發，否則中間時間極短又被認出來是個 Bot。
#
#
#
#
#
#
#
#
#
#
#
#
#
