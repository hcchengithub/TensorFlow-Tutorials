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
peforth.ok(loc=locals(),cmd=":> [0] constant main.locals : bye main.locals :> ['itchat'].logout() bye ; exit")  

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
        global nextDelay
        nextDelay_msg = '\nNext anti-robot delay time: %i seconds\n' % (nextDelay)
        if peforth.vm.debug==11: peforth.ok('11> ',loc=locals(),cmd=":> [0] constant loc11 cr")  # breakpoint    
        
        # re-direct the display to peforth screen-buffer
        peforth.vm.dictate("display-off")  
        try:
            # peforth.vm.dictate(cmd)
            peforth.ok('Console> ', loc=locals(),
                cmd=":> [0] constant console.locals " + cmd + " exit")
        except Exception as err:
            errmsg = "Failed! : {}".format(err)
            peforth.vm.dictate("display-on")
            send_chunk(errmsg + nextDelay_msg, msg.user.send)
        else:
            peforth.vm.dictate("display-on screen-buffer")
            screen = peforth.vm.pop()[0]
            send_chunk(screen + '\nOK\n' + nextDelay_msg, msg.user.send)

#        
# 讓 Inception V3 看照片，回答那啥。        
#        
def predict(msg):
    results = time.ctime() + '\n'
    results += 'Google Inception V3 thinks it is:\n'
    msg.download('download\\' + msg.fileName)  # 照片放在 working directory/download 下
    if peforth.vm.debug==22: peforth.ok('22> ',loc=locals(),cmd=":> [0] constant loc22 cr")  # breakpoint    
    if msg.fileName.strip().lower().endswith((".jpeg",'.jpg','.png')):
        pred = model.classify(image_path=('download\\'+ msg.fileName).strip())
        results += model.print_scores(pred=pred,k=10,only_first_name=True)
    else:
        results += 'Ooops! jpeg pictures only, please. {} is not one.\n'.format(msg.fileName)
    return results

@itchat.msg_register(ATTACHMENT, isGroupChat=True)
def _(msg):
    global nextDelay
    time.sleep(nextDelay)  # Anti-Robot delay 
    nextDelay = random.choice(range(3,18))
    nextDelay_msg = '\nNext anti-robot delay time: %i seconds\n' % (nextDelay)
    if peforth.vm.debug==33: peforth.ok('33> ',loc=locals(),cmd=":> [0] constant loc33 cr")  # breakpoint    
    if msg.user.NickName[:5]=='AILAB': # 只在 AILAB 工作，過濾掉其他的。
        msg.download('download\\' + msg.fileName)
        send_chunk('Attachment: %s \nreceived at %s\n' % (msg.fileName,time.ctime()) + nextDelay_msg, msg.user.send)

@itchat.msg_register(TEXT, isGroupChat=True)
def _(msg):
    if peforth.vm.debug==44: peforth.ok('44> ',loc=locals(),cmd=":> [0] constant loc44 cr")  # breakpoint    
    if msg.user.NickName[:5]=='AILAB': # 只在 AILAB 工作，過濾掉其他的。
        if msg.isAt: 
            time.sleep(nextDelay)  # Anti-Robot delay 
            cmd = msg.text.split("\n",maxsplit=1)[1] # remove the first line: @nickName ...
            console(msg, cmd)                        # 避免帶有空格的 nickName 惹問題

@itchat.msg_register(PICTURE, isGroupChat=True)
def _(msg):
    global nextDelay
    time.sleep(nextDelay)  # Anti-Robot delay 
    nextDelay = random.choice(range(3,18))
    nextDelay_msg = '\nNext anti-robot delay time: %i seconds\n' % (nextDelay)
    if peforth.vm.debug==55: peforth.ok('55> ',loc=locals(),cmd=":> [0] constant loc55 cr")  # breakpoint    
    if msg.user.NickName[:5]=='AILAB': # 只在 AILAB 工作，過濾掉其他的。
        send_chunk(predict(msg) + nextDelay_msg, msg.user.send)
    
itchat.auto_login(hotReload=False)
itchat.run(debug=False, blockThread=True)
peforth.ok('Examine> ',loc=locals(),cmd=':> [0] value locals')

# Bug list
# [x] 正常對話不需 delay --> FP @ v6
# [x] "Next anti-robot delay time" 往上合併好再發，
#     否則中間時間極短又被認出來是個 Bot。
#     --> FP @ v6
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
