#-*- coding:utf-8 -*-
import tkinter
import socket, threading

win = tkinter.Tk()  # 创建主窗口
win.title('服务器')
win.geometry("300x200+200+20")
users = {}#用户字典，也可以连接数据库
group = {}#多人聊天用户字典



def run(ck, ca):
    userName = ck.recv(1024)
    users[userName.decode("utf-8")] = ck#解码并储存用户的信息
    printStr = "" + userName.decode("utf-8") + "连接\n"#在连接显示框中显示是否连接成功
    text.insert(tkinter.INSERT, printStr)

    while True:
        rData = ck.recv(1024)
        dataStr = rData.decode("utf-8")
        infolist = dataStr.split(":")#分割字符串从而得到所要发送的用户名和客户端所发送的信息

        if(infolist[1]=="sendfile"):
            users[infolist[0]].send((userName.decode("utf-8") + ":" + infolist[1]+ ":" + infolist[2]+ ":" + infolist[3]).encode("utf"))
            file_size = int(infolist[2])
            received_size = 0
            while received_size < file_size:
                size = 0
                if file_size - received_size > 1024:  # 多次接收
                    size = 1024
                else:  # 最后一次接收完毕
                    size = file_size - received_size
                data = ck.recv(size)
                users[infolist[0]].send(data)
                data_len = len(data)
                received_size += data_len
        elif(infolist[0]=="add_in_group"):
            group[userName.decode("utf-8")] = users[userName.decode("utf-8")]
            for key in group:
                group[key].send(("GROUP_MESSAGE"+":"+userName.decode("utf-8") + "加入了群聊").encode("utf"))
        elif (infolist[0] =="quit_out_group"):
            for key in group:
                group[key].send(("GROUP_MESSAGE"+":"+userName.decode("utf-8") + "已经退出了群聊").encode("utf"))
            del group[userName.decode("utf-8")]
        elif (infolist[0] == "send_Group_Message"):
            if userName.decode("utf-8") in group:
                for key in group:
                    group[key].send(("GROUP_MESSAGE"+":"+userName.decode("utf-8")+":"+infolist[1]).encode("utf"))
        else:
            users[infolist[0]].send((userName.decode("utf-8") + ":" + infolist[1]).encode("utf"))
            #要发送信息的客户端向目标客户端发送信息

def start():
    ipStr = eip.get()#从输入端中获取ip
    portStr = eport.get()#从输入端中获取端口
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socked所准守ipv4或ipv6
    server.bind((ipStr, int(portStr)))#绑定ip和端口号！！！1:注意输入的端口号是str型而这里的要传入int型
    server.listen(10)
    printStr = "服务器启动成功\n"
    text.insert(tkinter.INSERT, printStr)#显示在信息窗口中
    while True:
        ck, ca = server.accept()
        t = threading.Thread(target=run, args=(ck, ca))
        t.start()


def startSever():
    s = threading.Thread(target=start)#启用一个线程开启服务器
    s.start()#开启线程

#下面是界面
labelIp = tkinter.Label(win, text='ip').grid(row=0, column=0)
labelPort = tkinter.Label(win, text='port').grid(row=1, column=0)
eip = tkinter.Variable()
eport = tkinter.Variable()
entryIp = tkinter.Entry(win, textvariable=eip).grid(row=0, column=1)
entryPort = tkinter.Entry(win, textvariable=eport).grid(row=1, column=1)
button = tkinter.Button(win, text="启动", command=startSever).grid(row=2, column=0)
text = tkinter.Text(win, height=7, width=30)
labeltext = tkinter.Label(win, text='连接消息').grid(row=3, column=0)
text.grid(row=3, column=1)
win.mainloop()

