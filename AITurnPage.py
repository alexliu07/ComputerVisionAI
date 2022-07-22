import pykeyboard,cv2
from core.handGestureMin import handGesture
#准备
winkeyboard = pykeyboard.PyKeyboard()
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
            # 获取食指关节y坐标
            if i['id'] == 6:
                index_pip_y = cy
            # 获取大拇指x,y坐标
            if i['id'] == 4:
                thumb_x = cx
                thumb_y = cy
            # 获取手指中部x坐标
            if i['id'] == 0:
                hand_x = cx
        # 手指于横向握拳状态
        if abs(index_pip_y - thumb_y) <= 15:
            # 大拇指在左边
            if thumb_x < hand_x:
                # 按下向左键
                winkeyboard.tap_key(37)
            # 大拇指在右边
            if thumb_x > hand_x:
                # 按下向右键
                winkeyboard.tap_key(39)