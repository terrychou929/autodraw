#moule=========================================================================
import cv2
import numpy as np
from copy import copy
import random
import turtle
from PIL import Image
import math

# cv2筆記
# image矩陣為三維矩陣，image[長,寬]=鎖定特定Pixel的RGB數值
# image = cv2.imread('testpics/4.jpg') #沒讀灰階
# cv2.imwrite('output1.jpg', image) #存檔
# parameters====================================================================

# general functions=============================================================
def resize(image,longest):
    height, width = image.shape
    
    if height >= width:
        nheight = longest
        nwidth = width*longest/height
    else:
        nwidth = longest
        nheight = height*longest/width        
    
    image = cv2.resize(image, (int(nwidth), int(nheight)))
    
    return(image,int(nwidth), int(nheight))

# functions====================================================================
def cny(image,param,blur,rsz,longest):
     
    # Canny’s algorithm for border detection is known as one of the most efficient
    # and fast methods to find discontinuity in digital images, producing as the 
    # processing result a binary image, which pixels are white for borders and 
    # black for everything else.
    print(image)
    if rsz:
        image,nwidth,nheight = resize(image,longest)
    
    # create blurs
    # 高斯模糊濾鏡通過平均像素值與其相鄰像素的值來平滑圖像。之所以稱為高斯模糊，是因為平均值具有高斯衰減效應
    if blur:
        image = cv2.GaussianBlur(image, (5, 5), 0)
    # print(image)
    # ratio: 2~3 is recomended
    ratio = 3 
    
    # param: the higher the param, the simpler the result 
    param = param + random.uniform(-1, 1)
    ratio = ratio + random.uniform(-1, 1)
    
    print("param: "+str(param),"ratio: "+str(ratio))
    
    image = cv2.Canny(image, param, param*ratio) 
    # print(image)
    # 影像二值化簡單的方法，如果像素值pixel大於門檻值threshold，就指定一個新數值(例如白色)，否則就指定另一個新數值(例如黑色)，
    ret,image = cv2.threshold(image,100,255,cv2.THRESH_BINARY_INV)
    # print(image)
    cv2.imshow("img",image)
    
    # cv2.imshow("canny", image)

    # display pciture
    cv2.waitKey(0)     
    cv2.destroyAllWindows()
    
    return(image,nwidth,nheight)

def pointilism(image,radius,rsz,longest,blur,video):

    # simply use cv2.circle to create pointilism creation
        #radius: 圓圈半徑 3~5 is recommended
        #deblur: remove blurs(True) will create a more clear result
    
    if rsz:
        image = resize(image,longest)[0]
 
    # create blurs
    # 高斯模糊濾鏡通過平均像素值與其相鄰像素的值來平滑圖像。之所以稱為高斯模糊，是因為平均值具有高斯衰減效應
    if blur:
        image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # e.g. 300x200 -> 長300，寬200，有300列array，每單列array裡面有200個值
    # print(image.shape)
    
    #step: 點間距 5 is recommended
    step = radius*5/3
    #rand: 原點抖動程度 3~4 is recommended
    rand = 3

    height, width = image.shape
    
    # copy a new image since we are going to utilize the original gray scale value
    points = copy(image)

    # clear canvas
    for i in range(height):
        for j in range(width):
            points[i, j] = 0

    # np.zero會返回用0填充的數組
    xrange = np.zeros(int(height/step))
    yrange = np.zeros(int(width/step))
    
    for xvalue in range(len(xrange)):
        xrange[xvalue] = xvalue
    
    for yvalue in range(len(yrange)):
        yrange[yvalue] = yvalue
    
    xrange = [value*step+step/2 for value in xrange]
    yrange = [value*step+step/2 for value in yrange]

    for i in xrange:
        for j in yrange:
            
            x = int(i + random.randint(1, rand))
            y = int(j + random.randint(1, rand))
            # print(x,y)
            
            if(x >= height):
                x = height-1
            if( y >= width):
                y = width-1
            gray = image[x,y]+random.randint(0, 5)
            
            # cv2.circle(圖像基底, 圓的中心座標, 圓的半徑, 圓的邊界顏色bgr, 圓邊界線的粗細像素, line type)
            cv2.circle(points,(y, x),radius,int(gray),-1,cv2.LINE_AA)
            
            if video:
                cv2.imshow("Canvas", points)
                cv2.waitKey(5)    

    if not video:
        
        cv2.imshow("Canvas", points)
        cv2.waitKey(0)                
        cv2.destroyAllWindows()

def greypic(image,rsz,longest):

    if rsz:
        image = resize(image,longest)[0]

    inverted = 255 - image       
    
    blur_image = cv2.GaussianBlur(inverted,(21,21),0)  
    
    inverted_blur = 255- blur_image
    sketch = cv2.divide(image,inverted_blur,scale=255)
    
    cv2.imshow("Canvas", sketch)
    cv2.waitKey(0)                
    cv2.destroyAllWindows()   

def distance(row,col,nrow,ncol):
    return((((nrow - row)**2) + ((ncol-col)**2) )**0.5)

def angle(v1,v2): 
    
    dx1 = v1[0]
    dy1 = v1[1]
    dx2 = v2[0]
    dy2 = v2[1]
    
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180/math.pi)

    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180/math.pi)

    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    
    return(included_angle)
    
def start_at(tt,width,height,row,col):
    
    #transform from image vector to turtle index

    tt.penup()
    
    x = col - width/2
    y = height/2 - row
    
    #turtle index
    tt.goto(x,y)
    
    return(tt, x, y)

def draw(tt,row,col,newrow,newcol):
    #row,newrow,col,newcol are turtle scale
    
    v1 = [1,0]
    v2 = [newrow-row,newcol-col]
    degree = angle(v1,v2)
    tt.right(degree)
    tt.pendown()
    d = distance(row,col,newrow,newcol)
    tt.forward(d)
    tt.penup()
    tt.left(degree)
    
    return(tt,newrow,newcol)
    
def reset(tt,screenwidth,screenheight):
    tt.penup()
    tt.goto(screenwidth/2, -screenheight/2)

def turtleindex(newrow,newcol,width,height):
    x = newcol - width/2
    y = height/2 - newrow
    
    return(x,y)

#turtle basics ==========================================================
turtletest = False
if turtletest:
    screenwidth = 500
    screenheight = 500

    screen = turtle.Screen()
    screen.setup(screenwidth, screenheight)
    
    tt = turtle.Turtle()
    tt.hideturtle()

    # start at left top
    
    for i in range(1,10):
        
        tt.pendown() 
        turtle.hideturtle()
        tt.forward(i)
        turtle.hideturtle()
        tt.penup()
        turtle.hideturtle()

    # screen.exitonclick() #keep screen
    
    ts = tt.getscreen()
    ts.getcanvas().postscript(file="sample.jpg") #svg檔, e.g: .ai, .eps
    
    # need ghostscript
    # im = Image.open("sample.eps") 
    # im.save("test.jpg", "JPEG") # transform svg to pixel file like jpg
    
    pass

#pending ====================================================================
canny = True
if canny:

    
    image = cv2.imread('testpics/4.jpg', cv2.IMREAD_GRAYSCALE) #有讀灰階
    image = cny(image,50,True,True,600)[0]
    
    #轉回RGB
    backtorgb = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    print(backtorgb) 
    backtorgb[0,0] = np.array([1,2,3])
    
    cv2.imshow("img",backtorgb)
    cv2.waitKey(0)     
    cv2.destroyAllWindows()    
    
point = False
if point:

    image = cv2.imread('testpics/4.jpg', cv2.IMREAD_GRAYSCALE)
    pointilism(image,4,False,500,False,False)

greypicture = False
if greypicture:

    image = cv2.imread('testpics/2.jpg', cv2.IMREAD_GRAYSCALE)
    greypic(image,True,500)

#main ====================================================================
history = []
threshold = 2**0.5
#turtle index
now_x = 0
now_y = 0

main = False
if main:
    
    image = cv2.imread('testpics/4.jpg', cv2.IMREAD_GRAYSCALE)
    
    # get image edge with gradient decent
    image,screenwidth,screenheight = cny(image,50,True,True,600)
    
    screen = turtle.Screen()
    screen.setup(screenwidth, screenheight)
    tt = turtle.Turtle()
    tt.speed(0)
    
    #loop through every row of the image
    for i in range(len(image)):  
        #loop through every column of the image
        for j in range(len(image[i])): 
            #if the pixel is black and not in drawing history
            if image[i][j]==0 and [i,j] not in history:
            
                history.append([i,j])  
                tt,now_x,now_y = start_at(tt, screenwidth, screenheight,i,j)
                
                if i < len(image)-1:
                    #jump to next row and start loop through every pixel
                    for k in range(i+1,len(image)):
                        chk = 0
                        for l in range(len(image[k])):  
                            tx,ty = turtleindex(k,l,screenwidth,screenheight)
                            
                            #if the pixel is black, and the distance between the pixel and previous pixel is less than threshold and not in drawing history
                            if image[k][l]==0 and distance(now_x,now_y,tx,ty)<=threshold and [k,l] not in history:
                                tt,now_x,now_y = draw(tt,now_x,now_y,tx,ty)
                                history.append([k,l]) 
                                chk = 1
                                break
                        if chk == 0:
                            reset(tt,screenwidth,screenheight)
                            break

    screen.exitonclick()



