import cv2,math
from core.handGestureMin import handGesture
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#开启摄像头
cap = cv2.VideoCapture(0)
#设置音量
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#获取音量最大与最小值
mini = volume.GetVolumeRange()[0]
maxi = volume.GetVolumeRange()[1]
#获取间距
vols = maxi - mini
while True:
    #读取图像
    success,img = cap.read()
    # 翻转图像
    img = cv2.flip(img, 1)
    #转换颜色
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #检测手部
    keyPos = handGesture(imgRGB)
    if keyPos:
        for i in keyPos:
            #检测食指坐标
            if i['id'] == 8:
                index_x = i['x']
                index_y = i['y']
            #检测大拇指坐标
            if i['id'] == 4:
                thumb_x = i['x']
                thumb_y = i['y']
        #获取两者距离
        distance = math.hypot(index_x - thumb_x,index_y - thumb_y)
        #保留三位小数
        newDis = round(distance,3)
        #求出要调整到的音量大小
        newVol = mini + (vols * newDis)
        #调整音量
        try:
            volume.SetMasterVolumeLevel(newVol, None)
        except Exception:
            volume.SetMasterVolumeLevel(maxi, None)