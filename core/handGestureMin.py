import mediapipe as mp
#创建手部识别模型
mpHands = mp.solutions.hands
hands = mpHands.Hands()
def handGesture(img):
    #进行手部识别
    results = hands.process(img)
    if results.multi_hand_landmarks:
        for i in results.multi_hand_landmarks:
            #返回手部坐标
            points = []
            for id,lm in enumerate(i.landmark):
                key = {'id':id,'x':lm.x,'y':lm.y}
                points.append(key)
            return points