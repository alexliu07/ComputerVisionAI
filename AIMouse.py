import cv2,pymouse,win32con,win32api
from core.handGestureMin import handGesture
#获取屏幕分辨率
scwidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scheight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
#开启键鼠控制
winmouse = pymouse.PyMouse()
#创建手指坐标变量
last_x = 'nothing'
last_y = 'nothing'
frame_delay = 'nothing'
final_index_x = None
final_index_y = None
#开启摄像头
cap = cv2.VideoCapture(0)
while True:
    #读取摄像头
    success , img = cap.read()
    #翻转图像
    img = cv2.flip(img, 1)
    #转换颜色
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #检测手掌
    keyPoints = handGesture(imgRGB)
    #转换坐标
    h , w , c = img.shape
    #cx：关键点的x坐标     cy：关键点的y坐标
    if keyPoints:
        for i in keyPoints:
            cx , cy = int(i['x'] * w) , int(i['y'] * h)
            #获取食指x,y坐标
            if i['id'] == 8:
                index_x_sc = int(i['x'] * (scwidth + 200))
                index_y_sc = int(i['y'] * (scheight + 500))
                index_x = cx
                index_y = cy
            #获取手掌底部y坐标
            if i['id'] == 1:
                wrist_y = cy
            #获取中指y坐标
            if i['id'] == 12:
                middle_y = cy
            #获取小拇指x坐标
            if i['id'] == 20:
                pinky_x = cx
        #移动鼠标
        winmouse.move(index_x_sc,index_y_sc)
        #判断点击
        #如果100帧以后位置相同则点击左键
        if frame_delay != 'nothing':
            if frame_delay == 0:
                first_index_x = index_x
                first_index_y = index_y
            frame_delay += 1
            if frame_delay == 30:
                final_index_x = index_x
                final_index_y = index_y
            if frame_delay == 45:
                frame_delay = 0
            if first_index_x and first_index_y and final_index_x and final_index_y:
                if abs(first_index_x - final_index_x) < 10 and abs(first_index_y - final_index_y) < 10:
                    winmouse.click(index_x_sc, index_y_sc, 1)
        else:
            frame_delay = 0