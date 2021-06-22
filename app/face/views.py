import cv2
import face_recognition
import os
import subprocess
import matplotlib.pyplot as plt
from flask import Flask,render_template,request,g
from . import face
from ..model import player

os.chdir(r'C:\Users\Bryce gu\Desktop\媒体大数据实例分析\欧洲杯球员识别\app')
number="1";

def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n
@face.route('/')
def go():
    return render_template('test.html')

@face.route('/index')
def index():
    return render_template('index.html')

@face.route('/cut')
def cut():
    wanted = request.args.get("wanted", type=str)
    v_path='static/'+wanted+'.mp4'
    #v_path='static/players.mp4'
    image_save='static/image'
    cap=cv2.VideoCapture(v_path)
    frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    _,img=cap.read()
    j=0
    for i in range(int(frame_count)-1):
        hash1 = dHash(img)
        _, img2 = cap.read()
        hash2 = dHash(img2)
        n = cmpHash(hash1, hash2)
        #print(n)
        if n>=35:
            j=j+1
            cv2.imwrite('static/image/{}.jpg'.format(j), img)
            img = img2
    cuts = os.listdir(image_save)
    cuts.sort(key=lambda x:int(x[:-4]))
    p='static/image'
    for i in range(len(cuts)):
        cuts[i]=p+'/'+cuts[i]
        print(cuts[i])
    return render_template('cut.html',result='Finish!',cuts=cuts,path=v_path)

@face.route('/match')
def match():
    try:
        number = request.args.get("wanted", type=str)
        print(number)
        if number == None:
            number = '1'
        path='static/players'
        players=os.listdir(path)
        flag=0
        for i in range(len(players)):
            known_path = path+'/'+players[i]
            unknown_path = "static/image/"+number+".jpg"
            known_image = face_recognition.load_image_file(known_path)
            unknown_image = face_recognition.load_image_file(unknown_path)
            # 获取
            known_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            # 将人脸编码列表与候选编码进行比较，看看它们是否匹配
            # tolerance低于设定的面与面之间的距离视为匹配，越低越严格。默认0.6为典型的最佳性能
            results = face_recognition.compare_faces([known_encoding],
                                                     unknown_encoding,
                                                     tolerance=0.6)
            if results[0]==True:
                flag=1
                name=players[i][:-4]
                print(name)
                res=list(player.query.filter(player.name.like('%'+name+'%')).all())
                rs=[{'name':row.name,'age':row.age,'nationality':row.nationality,'height':row.height} for row in res]
                print(rs)
                break
    except:
        # print(e)
        number = str(int(number) + 1)
        print(number)
        return render_template("match.html" ,outface=unknown_path,result="对不起，未能识别到人脸...",rs=[],number=number)

    else:
        if flag==1:
            number = str(int(number) + 1)
            print(number)
            return render_template('match.html', outface=unknown_path,result='球员匹配成功!',rs=rs[0],number=number)
        else:
            number = str(int(number) + 1)
            print(number)
            return render_template('match.html',outface=unknown_path,result='对不起，未能识别到球员...',rs=[],number=number)
