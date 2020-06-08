#-*- coding:utf-8 -*-
import tkinter
import socket
import threading
import os
import random

number=random.randint(0,9)
colorlist=["Wheat","AntiqueWhite","Beige","Skyblue","LightGrey","MistyRose","LightYellow","LightBlue","Thistle","LightPink"]
color=colorlist[number]



wins={} #是否创建了窗口
winstext={} #text缓存
win = tkinter.Tk()
win.title("客户端1")
win.geometry("1200x800+200+20")
win.configure(background=color)



ck = None#用于储存客户端的信息



def getInfo():
    while True:
        data = ck.recv(1024)#用于接受服务器发送的信息
        datastr=data.decode("utf-8")
        show=datastr+"\n"
        infolist = datastr.split(":")

        if(infolist[1]=="sendfile"):
            text.insert(tkinter.INSERT, "收到来自"+infolist[0]+"的文件\n")
            recvfile(infolist)

        elif(infolist[0]=="GROUP_MESSAGE"):
            try:
                groupstr=infolist[1]+"说"+infolist[2]+"\n"
                textgroupshow.insert(tkinter.INSERT,groupstr)
            except IndexError:
                groupstr="------------------"+infolist[1]+"--------------------\n"
                textgroupshow.insert(tkinter.INSERT, groupstr)

        else:
            text.insert(tkinter.INSERT, show)


def connectServer():
    global ck
    ipStr = eip.get()
    portStr = eport.get()
    userStr = euser.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6
    client.connect((ipStr, int(portStr)))#连接ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    client.send(userStr.encode("utf-8"))
    ck = client

    t = threading.Thread(target=getInfo)
    t.start()

def sendfile():
    filename = esendfile.get()
    friend = efriend2.get()
    size = os.stat(filename).st_size # 获取文件大小
    gettype=filename.split(".")
    typeOfFile=gettype[-1:]
    typeoffile="".join(typeOfFile)
    seq = (friend,"sendfile",str(size),typeoffile)
    sendStr =":".join(seq)
    ck.send(sendStr.encode("utf-8"))  # 发送数据长度
    f = open(filename, "rb")
    for line in f:
        ck.send(line)  # 发送数据
    f.close()

def recvfile(infolist):
    # 1.接收长度
    file_size = int(infolist[2])
    file_type=infolist[3]

    # 2.接收文件内容
    filename = "new."+file_type

    f = open(filename, "wb")
    received_size = 0

    while received_size < file_size:
        size = 0  # 准确接收数据大小，解决粘包
        if file_size - received_size > 1024:  # 多次接收
            size = 1024
        else:  # 最后一次接收完毕
            size = file_size - received_size

        data = ck.recv(size)  # 多次接收内容，接收大数据
        data_len = len(data)
        received_size += data_len
        f.write(data)
    f.close()



def sendMail():
    friend = efriend.get()
    sendStr = esend.get()
    sendStr = friend + ":" + sendStr
    ck.send(sendStr.encode("utf-8"))

def addgroup():
    sendStr="add_in_group"+ ":" +"add_in_group"
    ck.send(sendStr.encode("utf-8"))

def quitgroup():
    sendStr="quit_out_group"+ ":" +"quit_out_group"
    ck.send(sendStr.encode("utf-8"))

def sendGroupMessage():
    sendStr = echat.get()
    sendStr = "send_Group_Message" + ":" + sendStr
    ck.send(sendStr.encode("utf-8"))



#下面是界面

labelUse = tkinter.Label(win, text="userName",bg=color).place(x = 40, y =30, width=60, height=24)


euser = tkinter.Variable()
entryUser = tkinter.Entry(win, textvariable=euser).place(x = 120, y = 30 , width=254, height=21)

labelIp = tkinter.Label(win, text="ip",bg=color).place(x = 40, y =70, width=60, height=24)
eip = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eip).place(x = 120, y = 70 , width=254, height=21)

labelPort = tkinter.Label(win, text="port",bg=color).place(x = 40, y =110, width=60, height=24)
eport = tkinter.Variable()

entryPort = tkinter.Entry(win, textvariable=eport).place(x = 120, y = 110 , width=254, height=21)

button = tkinter.Button(win, text="登陆", command=connectServer).place(x = 80, y = 150 , width=63, height=33)

historysend = tkinter.Label(win, text="历史信息",bg=color).place(x = 580, y = 250 , width=60, height=26)
text = tkinter.Text(win, height=494, width=484)
text.place(x=670,y=50, height=494, width=484)

esend = tkinter.Variable()
labelesend = tkinter.Label(win, text="发送消息",bg=color).place(x = 630, y = 590 , width=60, height=26)
entrySend = tkinter.Entry(win, textvariable=esend).place(x = 700, y = 590 , width=184, height=21)

efriend = tkinter.Variable()
labelefriend= tkinter.Label(win, text="发给谁",bg=color).place(x = 630, y = 630 , width=60, height=26)
entryFriend = tkinter.Entry(win, textvariable=efriend).place(x = 700, y = 630 , width=184, height=21)

button2 = tkinter.Button(win, text="发送消息", command=sendMail).place(x = 700, y = 660 , width=63, height=33)

#发送文件
esendfile = tkinter.Variable()
labelesendfile = tkinter.Label(win, text="文件目录",bg=color).place(x = 895, y = 590 , width=60, height=26)
entrySendfile = tkinter.Entry(win, textvariable=esendfile).place(x = 960, y = 590 , width=184, height=21)

efriend2 = tkinter.Variable()
labelefriend2= tkinter.Label(win, text="发给谁",bg=color).place(x = 895, y = 630 , width=60, height=26)
entryFriend2 = tkinter.Entry(win, textvariable=efriend2).place(x = 960, y = 630 , width=184, height=21)

button3 = tkinter.Button(win, text="发送文件", command=sendfile).place(x = 960, y = 660 , width=63, height=33)

#群聊
labelgroup = tkinter.Label(win, text="群聊消息",bg=color).place(x = 50, y =260, width=60, height=26)

textgroupshow = tkinter.Text(win, height=494, width=394)
textgroupshow.place(x=50,y=290, height=394, width=494)

buttonadd = tkinter.Button(win, text="加入群聊", command=addgroup).place(x = 50, y = 690 , width=63, height=33)
buttonquit = tkinter.Button(win, text="退出群聊", command=quitgroup).place(x = 50, y = 730 , width=63, height=33)
labelmessage = tkinter.Label(win, text="发送消息",bg=color).place(x = 160, y =700, width=60, height=26)

buttonchat = tkinter.Button(win, text="发送", command=sendGroupMessage).place(x = 230, y = 730 , width=63, height=33)
echat = tkinter.Variable()
entrygroupchat = tkinter.Entry(win, textvariable=echat).place(x = 230, y = 700 , width=224, height=21)



win.mainloop()
