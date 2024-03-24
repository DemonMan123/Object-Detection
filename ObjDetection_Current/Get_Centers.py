def getCenter_rectangle(x1,y1,x2,y2):
    Center_X, Center_Y = ((x1+x2)/2, (y1+y2)/2)
    return int(Center_X),int(Center_Y)

def GetCenter_frame(width,height):
    w = width//2
    h = height//2
    return int(w),int(h)