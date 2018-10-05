import numpy as np
import cv2
import cvui
import imutils
import math
import PIL.Image
import time
import os
from tkinter.filedialog import askopenfilename
import Tkinter as tk
import yaml

width, height = 3264, 2448
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

filename=" "
flag=" "

totalcell=0
outera=0.0
innera=0.0

with open("data.yaml", 'r') as stream:
    data = yaml.load(stream)

print data
cellv1=data["cellv1"]
cellv2=data["cellv2"]
cellv3=data["cellv3"]
cella1=data["cella1"]
cella2=data["cella2"]
inv1=data["inv1"]
inv2=data["inv2"]
inv3=data["inv3"]
ina1=data["ina1"]
ina2=data["ina2"]
outv1=data["outv1"]
outv2=data["outv2"]
outv3=data["outv3"]
outa1=data["outa1"]
outa2=data["outa2"]
cellis=data["celli"]
inis=data["ini"]
outis=data["outi"]
mmpp=data["mmpp"]
pxd=data["pxd"]
actualdis=data["actualdis"]
'''celli=0
ini=0
outi=0
Value1=0.
cellv1=[0.]
cellv2=[0.]
cellv3=[0.]
cella1=[500.]
cella2=[600.]
inv1=[0.]
inv2=[0.]
inv3=[0.]
ina1=[500.]
ina2=[6000.]
outv1=[0.]
outv2=[0.]
outv3=[0.]
outa1=[500.]
outa2=[6000.]


Value1 = [100]
Value2 = [255]
Value3 = [0]
a1=[100]
a2=[10000]'''

mainwindow = "Main Window"
settingwindow="Settings"
testingwindow="Testing"
frame1 = np.zeros((600, 700, 3), np.uint8)

frame2 = np.zeros((400, 600, 3), np.uint8)
frame3 = np.zeros((700, 600, 3), np.uint8)


def OpenFile():
    tk.Tk().withdraw()


    namef = askopenfilename(initialdir=os.getcwd(),
                           filetypes =(("Image file", "*.jpg"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    print (namef)
    global flag
    if(namef==""):
        flag=" "
    else:
        flag="f"
        global filename
        filename =namef
    #show_frame1()

def viewimg(fn,title):
    img=cv2.imread(fn)
    [y,x,a]=img.shape
    r=1.0
    while ((y/r)>640):
        r=r+.1
    img = cv2.resize(img, (int(x/r), int(y/r)))
    cv2.imshow(title,img)

def camera():


    _, frame1 = cap.read()
    [y,x,a]=frame1.shape
    r=1
    while ((y/r)>640):
        r=r+.1
    print r
    while True:

        _, frame = cap.read()
        _, framed = cap.read()
        k=cv2.waitKey(20)
        frame = cv2.resize(frame, (int(x/r), int(y/r)))
        cv2.imshow("Camera",frame)
        if k== 32:
            cv2.imwrite("capture.jpg",framed)
            cv2.destroyWindow("Camera")
            global filename
            global flag
            filename="capture.jpg"
            flag="cam"
            cv2.destroyWindow("Rcamera")
            break
        if k == 27:
            cv2.destroyWindow("Camera")
            cv2.destroyWindow("Rcamera")
            break

def thresh(fn,v1,v2,v3,i):
    img=cv2.imread(filename)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray,v1,v2,v3)
    
    if(i==True):
        thresh = (255-thresh)
        #ret,thresh = cv2.threshold(thresh,110,225,0)
    cv2.imwrite('tre.jpg',thresh)
def showarea(fn,v1,v2,v3,i,mia,mxa,s,pr,tos):
    global totalcell
    global outera
    global innera
    thresh(fn,v1,v2,v3,i)
    threshf=cv2.imread('tre.jpg',0)
    img=cv2.imread(fn)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #ret,threshf = cv2.threshold(threshf,100,225,0)

    #cv2.imwrite("test.jpg",threshf)
    im2,cnts,hierarchy = cv2.findContours(threshf, 1, 2)
    count=0
    laa=0
    totalarea=0
    if(tos=="t" and s!=1):
        fimg=cv2.imread("final.jpg")

    

    for c in cnts:
        area = cv2.contourArea(c)
        if(area>laa):
            laa=area

        if ( area>mia and area<mxa ):
            count+=1
            if(pr==1):
                print area
            if(s==1):

                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img,[box],0,(0,0,255),2)
                
            if(s==2 or s==3):
                (x1,y1),radius = cv2.minEnclosingCircle(c)
                center = (int(x1),int(y1))
                radius = int(radius)
                if(s==3):
                    totalarea+=area
                    print radius
                    print area
                    print "...."
                if(tos=="t"):
                    cv2.circle(fimg,center,radius,(225,0,0),5)
                    cv2.circle(fimg,center,5,(225,0,0),-1)
                cv2.circle(img,center,radius,(225,0,0),5)
                cv2.circle(img,center,5,(225,0,0),-1)
    if(tos=="t" ):
        if(s==1):
            
            cv2.putText(img,'Number of cells='+str(count),(5,60), font, 2,(255,0,255),3,cv2.LINE_AA)
            cv2.imwrite("final.jpg",img)
            totalcell=count
            
        if(s==2):
            cv2.imwrite("final.jpg",fimg)
            outera=3.14*radius**2
            print "Radius"+str(radius*mmpp)
            
        if(s==3):
            innera=totalarea
            tinarea=innera*mmpp*mmpp
            toutarea=outera*mmpp*mmpp
            tcellparea=totalcell/((outera-innera)*mmpp*mmpp)

            cv2.putText(fimg,'Inner area='+str(tinarea),(5,120), font, 2,(100,60,255),3,cv2.LINE_AA)
            cv2.putText(fimg,'outer area='+str(toutarea),(5,180), font, 2,(0,255,100),3,cv2.LINE_AA)
            cv2.putText(fimg,'cell per area ='+str(tcellparea),(5,240), font, 2,(255,10,155),3,cv2.LINE_AA)
            
            cv2.imwrite("final.jpg",fimg)
            
            print "outer area"+str(outera*mmpp*mmpp)
            print "inner area"+str(innera*mmpp*mmpp)
            print "total cells = "+str(totalcell)
            print "cell per area = "+str(totalcell/((outera-innera)*mmpp*mmpp))
            
    print "largest area = " +str(laa)
    print "Total under the limits " +str(count)
    cv2.imwrite("markedarea.jpg",img)
x1=0
x2=0
y1=0
y2=0

def setpoint(event,x,y,flags,param):
    global x1
    global x2
    global y1
    global y2
    #print x,y
    global filename
    global rr
    img=cv2.imread(filename)
    global pxd
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),2,(255,0,0),-1)
        cv2.imshow('calibration',img)
        if x1==0:
            x1=x
            y1=y
        elif x2==0:
            x2=x
            y2=y
            
            print x1,y1,x2,y2
            cv2.circle(img,(x1,y1),2,(255,0,0),-1)
            cv2.imshow('calibration',img)
            
            pxd=math.sqrt(((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))
            if(rr>1):
                pxd=math.sqrt(((x1-x2)*rr)**2+((y1-y2)*rr)**2)
                
            
            print 'ditance between two ponts in pexels'
            print pxd
            
        elif y2>0:
            #global img
            img=cv2.imread(filename)
            cv2.imshow('calibration',img)
            x1=0
            y1=0
            x2=0
            y2=0

rr=1.0
def distancecalibration(filen):
    global rr
    global mmpp
    global actualdis
    global filename
    #actualdis=input("Enter the actual distance in mm ")
    img=cv2.imread(filen)
    [y,x,a]=img.shape
    cv2.imshow('calibration',img)
    i=1
    flagcal=0
    while(1):
        
        k = cv2.waitKey(10) & 0xFF
        if(k==32):
            rr=1.0
            while ((y/rr)>640):
                rr=rr+.1
            img = cv2.resize(img, (int(x/rr), int(y/rr)))
            cv2.imwrite("resize.jpg",img)
            cv2.imshow('calibration',img)
            
            filename="resize.jpg"
            flagcal=2
                 
        cv2.namedWindow('calibration')
        cv2.setMouseCallback('calibration',setpoint)
        if k == 27:
            cv2.destroyWindow("calibration")
            filename=filen
            break
    mmpp=actualdis/pxd
    if(flagcal==2):
        mmpp=actualdis/pxd
    print "mm per pixel"
    print mmpp



cvui.init(mainwindow)
while True:
    '''global mmpp
    global actualdis
    global pxd'''
    frame1[:] = (49, 52, 49)
    cvui.text(frame1, 268, 584, 'Developed by Verifygn')
    if cvui.button(frame1, 295, 300, "  Testing  "):
        print "testing"
        cv2.destroyWindow("Main Window")
        cvui.init(testingwindow)
        flag==" "
        while(1):
            k = cv2.waitKey(10) & 0xFF
            frame2[:] = (49, 52, 49)
            if cvui.button(frame2, 100,1, 'Browse.'):
                print "..."
                OpenFile()
                img1=cv2.imread(filename)

            if cvui.button(frame2, 1,1, 'camera'):
                print "Camera"
                camera()
            if(flag=="f" or flag =="cam"):
                if cvui.button(frame2, 1,100, 'Calculate'):
                    showarea(filename,int(cellv1[0]),int(cellv2[0]),int(cellv3[0]),cellis[0],int(cella1[0]),int(cella2[0]),1,0,"t")
                    showarea(filename,int(outv1[0]),int(outv2[0]),int(outv3[0]),outis[0],int(outa1[0]),int(outa2[0]),2,0,"t")
                    showarea(filename,int(inv1[0]),int(inv2[0]),int(inv3[0]),inis[0],int(ina1[0]),int(ina2[0]),3,0,"t")
                    viewimg("final.jpg","result")
                    
                



            

            cvui.imshow(testingwindow, frame2)
            if k == 27:
                cv2.destroyWindow("result")
                cv2.destroyWindow("Testing")
                cvui.init(mainwindow)
                break



    if cvui.button(frame1, 295, 200, "  settings  "):
        print "setting"
        cv2.destroyWindow("Main Window")
        cvui.init(settingwindow)
        
        '''cellis =[False]
        outis=[False]
        inis=[False]'''
        pst=[False]
        
        


        pst=[False]
        while(1):
            k = cv2.waitKey(10) & 0xFF
            frame3[:] = (49, 52, 49)
            if cvui.button(frame3, 100,1, 'Browse.'):
                print "..."
                OpenFile()
                img1=cv2.imread(filename)

            if cvui.button(frame3, 1,1, 'camera'):
                print "Camera"
                camera()
                #cvui.init(settingwindow)
            if(flag=="f" or flag =="cam" or flag=="th"):
                if(flag=="f" or flag =="cam"):
                    cv2.destroyWindow("thresh")
                    viewimg(filename,"view")

                if(flag=='th'):
                    cv2.destroyWindow("view")
                    


                

                cvui.text(frame3, 1, 30, 'cell')
                cvui.trackbar(frame3, 5, 40, 300,cellv1, 0, 255)
                cvui.trackbar(frame3, 300, 40, 300,cellv2, 0, 255)
                cvui.trackbar(frame3, 5, 90, 300,cellv3, 0, 255)
                cvui.checkbox(frame3, 450, 90, 'invert', cellis)
                cvui.trackbar(frame3, 5, 140, 300,cella1, 200,10000)
                cvui.trackbar(frame3, 5, 195, 300,cella2, 200, 15000)



                cvui.text(frame3, 1, 240, 'outer dia')
                cvui.trackbar(frame3, 5, 250, 300,outv1, 0, 255)
                cvui.trackbar(frame3, 300, 250, 300,outv2, 0, 255)
                cvui.trackbar(frame3, 5, 300, 300,outv3, 0, 255)
                cvui.checkbox(frame3, 450, 300, 'invert', outis)
                cvui.trackbar(frame3, 5, 350, 300,outa1, 200, 190000)
                cvui.trackbar(frame3, 5, 400, 300,outa2, 10000, 5000000)


                cvui.text(frame3, 1, 445, 'inner dia')
                cvui.trackbar(frame3, 5, 455, 300,inv1, 0, 255)
                cvui.trackbar(frame3, 300, 455, 300,inv2, 0, 255)
                cvui.trackbar(frame3, 5, 505, 300,inv3, 0, 255)
                cvui.checkbox(frame3, 450, 505, 'invert', inis)
                cvui.trackbar(frame3, 5, 555, 300,ina1, 200,80000)
                cvui.trackbar(frame3, 5, 605, 300,ina2, 200, 100000)


                if cvui.button(frame3, 400,140, 'Preview1'):

                    thresh(filename,int(cellv1[0]),int(cellv2[0]),int(cellv3[0]),cellis[0])
                    viewimg("tre.jpg","thresh")
                    flag="th"
                    print "preview"

                if cvui.button(frame3, 400,320, 'Preview2'):
                    thresh(filename,int(outv1[0]),int(outv2[0]),int(outv3[0]),outis[0])
                    viewimg("tre.jpg","thresh")
                    flag="th"
                    print "preview"

                if cvui.button(frame3, 400,550, 'Preview3'):
                    thresh(filename,int(inv1[0]),int(inv2[0]),int(inv3[0]),inis[0])
                    viewimg("tre.jpg","thresh")
                    flag="th"
                    print "preview"

                cvui.checkbox(frame3, 5, 660, 'print', pst)

                if pst[0]==True:
                    p=1
                else:
                    p=0

                if cvui.button(frame3, 400,190, 'show area1'):
                    showarea(filename,int(cellv1[0]),int(cellv2[0]),int(cellv3[0]),cellis[0],int(cella1[0]),int(cella2[0]),1,p,"s")
                    viewimg("markedarea.jpg","detected")
                    flag="th"

                if cvui.button(frame3, 400,370, 'show area2'):
                    showarea(filename,int(outv1[0]),int(outv2[0]),int(outv3[0]),outis[0],int(outa1[0]),int(outa2[0]),2,p,"s")
                    viewimg("markedarea.jpg","detected")
                    flag="th"

                if cvui.button(frame3, 400,590, 'show area2'):
                    showarea(filename,int(inv1[0]),int(inv2[0]),int(inv3[0]),inis[0],int(ina1[0]),int(ina2[0]),3,p,"s")
                    viewimg("markedarea.jpg","detected")
                    flag="th"

                if cvui.button(frame3, 280,660, 'calibration'):
                    distancecalibration(filename)
                cvui.text(frame3, 160, 665, str(actualdis))
                   # pr=ad/pxd
                if cvui.button(frame3, 110,660, '-'):
                    actualdis=actualdis-1
                if cvui.button(frame3, 190,660, '+'):
                    actualdis=actualdis+1
                mmpp=actualdis/pxd
                cvui.text(frame3, 400, 680, str(mmpp))

                if cvui.button(frame3, 400,620, 'save'):
                    '''print cellv1,cellv2,cellv3,cella1,cella2,celli
                    print "in"
                    print inv1,inv2,inv3,ina1,ina2,ini
                    print "out"
                    print outv1,outv2,outv3,outa1,outa2,outi'''
                    data={"cellv1":cellv1,"cellv2":cellv2,"cellv3":cellv3,"cella1":cella1,"cella2":cella2,"inv1":inv1,"inv2":inv2,"inv3":inv3,"ina1":ina1,"ina2":ina2,
                          "outv1":outv1,"outv2":outv2,"outv3":outv3,"outa1":outa1,"outa2":outa2,"celli":cellis,"ini":inis,"outi":outis,"mmpp":mmpp,"pxd":pxd,
                          "actualdis":actualdis}
                    fname = "data.yaml"
                    with open(fname, "w") as f:
                        yaml.dump(data, f)
                    print "all saved"


                if cvui.button(frame3, 480,620, 'reset'):

                    with open("data.yaml", 'r') as stream:
                        data = yaml.load(stream)

                    print data
                    cellv1=data["cellv1"]
                    cellv2=data["cellv2"]
                    cellv3=data["cellv3"]
                    cella1=data["cella1"]
                    cella2=data["cella2"]
                    inv1=data["inv1"]
                    inv2=data["inv2"]
                    inv3=data["inv3"]
                    ina1=data["ina1"]
                    ina2=data["ina2"]
                    outv1=data["outv1"]
                    outv2=data["outv2"]
                    outv3=data["outv3"]
                    outa1=data["outa1"]
                    outa2=data["outa2"]
                    celli=data["celli"]
                    ini=data["ini"]
                    outi=data["outi"]
                    pxd=data["pxd"]
                    actualdis=data["actualdis"]
                    print "all reset"



            cvui.imshow(settingwindow, frame3)
            if k == 27:
                cv2.destroyWindow("detected")
                cv2.destroyWindow("Settings")
                cv2.destroyWindow("view")
                cv2.destroyWindow("thresh")
                cvui.init(mainwindow)
                break





    cvui.imshow(mainwindow, frame1)
    if cv2.waitKey(20) == 27:
        break
cv2.destroyAllWindows()
