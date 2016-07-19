from tornado import ioloop, web, websocket, template, httpserver
#from Tkinter import * # GUI 
from pytribe import *
import sys, json
from tornado.ioloop import PeriodicCallback
import math  # for sqrt()
import thread
import time
###
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# The colormap
cmap = cm.jet
PointNumPerImage=250
ImageNumPerFolder=10
start_bool=0
###
"""
tornado is for Websocket server set
"""
tracker=EyeTribe()
server = None
Next_Page_Button = [-1.0, -1.0, -1.0, -1.0]
Prev_Page_Button = [-1.0, -1.0, -1.0, -1.0]
border = 100

class WSHandler(websocket.WebSocketHandler):
  
    def open(self):
        print "open"
        global cntNex
        global cntPre
        global cntHig
        global regPt
        global gaze
        global gazing
        global gazePt
        global Prevbool
        global Nextbool
        global clock
###
        global screen_x, screen_y
        global fig, p_pre, continuous, n_continuous
        global gX, gY
        global point_cnt, image_cnt
        global ax
        global start_bool
###
        regPt = (-1.0,-1.0)
        cntNex = 0
        cntPre = 0
        cntHig = 0
        gaze = False
        gazing = 0
        gazePt = (-1.0, -1.0)
        n_continuous=0 
        p_pre = (2000, 2000)
        continuous=0 
        Prevbool=1
        Nextbool=0
        clock = 0
        self.callback = PeriodicCallback(self.send_SDKdata, 50)
        self.callback.start()

    def send_SDKdata(self):
        global cntNex
        global cntPre
        global cntHig
        global regPt
        global gaze
        global gazing
        global gazePt
        global p_pre, continuous, n_continuous
        global Prevbool
        global Nextbool
        global clock
###
        global screen_x, screen_y
        global fig
        global gX, gY
        global point_cnt, rainbow, image_cnt
        global ax
        global start_bool
###
        if start_bool==0:
            return
        if Prevbool == False: #or Nextbool == False:
            clock = clock+1
            if clock == 10:
                clock = 0
                Prevbool = True
                #Nextbool = True
        
	# the more gazing signal, we can consider the user is gaze at a point
	#start record gaze
        tracker.start_recording()
	# we define the gaze() in "Eyetribe" class, return "fix"=> true or false
      
      #testing
        #pt = tracker.sample()
        if tracker.gaze(): 
            # we define the sample() in "Eyetribe" class, return (x,y)
            pt = tracker.sample()
            
            if gazePt[0] < 0: # initial time
                gazePt = pt
            # avoid blink pt=( 0.0, 0.0 )
            if pt[0] < 0.0001 and pt[0] > -0.0001 and pt[1] < 0.0001 and pt[1] > -0.0001:
                pt = regPt
            else:
                regPt = pt
                
            distance = math.sqrt((gazePt[0] - pt[0])**2 + (gazePt[1] - pt[1])**2)
            print "distance: ",distance
            if gazing == 5:
                gaze = True
                #regPt = gazePt # record the true position 
                #print "!!!!!!!!!!!!!!UPDATE regPt-> gaze = True!!!!!!!!!!!!!!!" # check whether update so slow!~
            elif distance < 50.0:
                gazing += 1
                gazePt = ((gazePt[0] + pt[0]) / 2, (gazePt[1] + pt[1]) / 2)
            elif gazing > 0:
                gazing -= 1
            else: # gazing==0
                gaze = False
                gazePt = pt
        else:
            if gazing == 0: 
                gaze = False
                gazePt = tracker.sample()
            else:
                gazing -= 1
                if gazePt[0]<0:
                    gazePt = tracker.sample()

        #///////////////////////////////////////////////////#  
       
        message = {"com":'Highlight',"x": gazePt[0],"y": gazePt[1]}  
        if gazePt[0]>=Prev_Page_Button[0]-border and gazePt[0]<=Prev_Page_Button[1]+border and gazePt[1]>=Prev_Page_Button[2]-border and gazePt[1]<=Prev_Page_Button[3]+border and gaze and Prevbool:
            cntPre=cntPre+1
            cntNex=0
            cntHig=0
            if cntPre==10: # 1.7 seconds
                print "////////////Turn to Previous Page."
                # set previous page message.
                message = {"com":'Previous'} 
                cntPre=0
                Prevbool=0
            else: 
                print "Highlight.+ Pre count."
                #message = {"com":'Highlight',"x": gazePt[0],"y": gazePt[1]}        
        #////////////////////////// # 
        print "@n_continuous: " , n_continuous
        if gazePt[0]>p_pre[0]+5 and gazePt[1]>=Next_Page_Button[2]-border and gazePt[1]<=Next_Page_Button[3]+border:
            n_continuous = n_continuous + 5
            
            if n_continuous > 20: #continuous for # points
                Nextbool = 1              
                if gazePt[0]>=Next_Page_Button[0]-border and gazePt[0]<=Next_Page_Button[1]+border and gazePt[1]>=Next_Page_Button[2]-border and gazePt[1]<=Next_Page_Button[3]+border and Nextbool:                 
                    message = {"com":'Next'}
                    Nextbool=0
                    n_continuous = 0
                    
                    """
                    cntNex=cntNex+1
                    cntPre=0
                    cntHig=0
                    #print "/////////////Nex count: ",cntNex
                    if cntNex==10: # 1.7 seconds
                        print "Turn to Next Page.////////////"
                        # set next page message.
                        message = {"com":'Next'} 
                        cntNex=0
                        Nextbool=0
                        n_continuous = 0
                    #else: 
                        #print "Highlight.+ Nex count."
                        #message = {"com":'Highlight',"x": gazePt[0],"y": gazePt[1]}       
                    """
            else:
                    cntHig=cntHig+1
                    if cntHig>=20:
                        cntPre=0
                        cntNex=0
                        cntHig=0
                    print "Highlight."
                    #message = {"com":'Highlight',"x": gazePt[0],"y": gazePt[1]}   
        elif gazePt[1]>Next_Page_Button[2]+border or gazePt[1]<Next_Page_Button[3]-border:
            if n_continuous >0 :
                n_continuous = n_continuous-1
            print "minus continuous: ", n_continuous
            cntHig=cntHig+1
            if cntHig>=20:
                cntPre=0
                cntNex=0
                cntHig=0
            #print "Highlight."
            #message = {"com":'Highlight',"x": gazePt[0],"y": gazePt[1]}
        p_pre = gazePt
        #/////////////////////////// #  

        
      # send the message to server
        #print >>sys.stderr, 'sending "%s"' % message
        self.write_message(json.dumps(message))     

        # end record gaze
        tracker.stop_recording()
          
      
    def on_message(self, message):
        global Prevbool
        global Nextbool
###
        global screen_x, screen_y, ax, fig
        global start_bool
        start_bool=1
###
        data= json.loads(message)
        print >>sys.stderr, 'received "%s"' % data    
###
        # first step: find the following two Button site while connext to Javascript UI  
        if data['status']=="CONNECTED" or data['status']=="RESIZED":
###
            # Next_Page_Button=[xmin xmax ymin ymax]
            Next_Page_Button[0] = data['nextX0']
            Next_Page_Button[1] = data['nextX1']
            Next_Page_Button[2] = data['nextY0']
            Next_Page_Button[3] = data['nextY1']
            # Prev_Page_Button=[xmin xmax ymin ymax]
            Prev_Page_Button[0] = data['prevX0']
            Prev_Page_Button[1] = data['prevX1']
            Prev_Page_Button[2] = data['prevY0']
            Prev_Page_Button[3] = data['prevY1']
###
            # screen x & y
            screen_x=data['screenX']
            screen_y=data['screenY']
            ax.set_xlim(0., int(screen_x))
            ax.set_ylim(0., int(screen_y))
            ax.set_ylim(ax.get_ylim()[::-1])
###
        #print "NX: ",Next_Page_Button
        #print "PV: ",Prev_Page_Button

    def on_close(self):
        self.callback.stop()

  # for fixing 403 error    
    def check_origin(self,origin): # default is "False"-> need return True  
        return True

def serve_forever():
    global server
    application = web.Application([
      (r'/ws', WSHandler),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(80)
    print('Server listening at http://your.domain.example:80/')
    server = ioloop.IOLoop.instance().start()

def drawRecords(string, sleeptime, *args):
    global gazePt, ax, gX, gY, point_cnt, image_cnt, screen_x, screen_y, start_bool, fig
    #print "XXXXXXXXXXXXXXXXXX"
    while(True):
        time.sleep(sleeptime)
        #print "start_bool: ", start_bool
        if start_bool == 0: 
            continue
        else:
            ###
            #print "DDDDDDDDDDDDDDDDDDDDDDDDdraw EyeMap picture"
            if ((gazePt[0]<=0.1 and gazePt[0]>=-0.1) and (gazePt[1]<=0.1 and gazePt[1]>=-0.1)) or gazePt[0]>screen_x or gazePt[0]<0.0 or gazePt[1]>screen_y or gazePt[1]<0.0: 
                continue
            else:
                if len(gX)==0:
                    print "point_cnt: ", point_cnt # when undfined point-> dont plus!!
                    gX.append(gazePt[0])
                    gY.append(gazePt[1])
                    point_cnt=point_cnt+1
                else:
                    if gazePt[0]>gX[0]+5 or gazePt[0]<gX[0]-5 or gazePt[1]>gY[0]+5 or gazePt[1]<gY[0]-5:
                        print "point_cnt: ", point_cnt # when undfined point-> dont plus!!
                        gX.append(gazePt[0])
                        gY.append(gazePt[1])
                        point_cnt=point_cnt+1
                        if len(gX)==2:
                            rainbow = cmap(int(255-np.rint((float(point_cnt-1)/PointNumPerImage)*255))) # float/int-> 0.xxxxxxxxxxxx(.12 digits)
                            ax.plot(gX, gY, linestyle="-", linewidth=5.0, color=rainbow)
                            ax.hold(True)
                            gX=[]
                            gY=[]
                            plt.gca().set_aspect('equal', adjustable='box') # adjustable='box'? make units square!!!
                            output = plt.gcf()
                            plt.draw() 
                            if point_cnt==PointNumPerImage:
                                print "image_cnt: ",image_cnt
                                imName = 'EyeMap_%s' % str(image_cnt)
                                output.savefig('%s.png' % imName) 
                                image_cnt=image_cnt+1
                                if image_cnt==ImageNumPerFolder:
                                    image_cnt=0
                                ax.cla()
                                ax.set_xlim(0., int(screen_x))
                                ax.set_ylim(0., int(screen_y))
                                ax.set_ylim(ax.get_ylim()[::-1])
                                point_cnt=0
                            else:
                                gX.append(gazePt[0])
                                gY.append(gazePt[1])
 ###              

if __name__ == '__main__':
    global fig, ax, screen_x, screen_y, gX, gY, point_cnt, image_cnt, start_bool
    start_bool=0
    gX=[]
    gY=[]
    point_cnt=0
    image_cnt=0
    fig = plt.figure()
    ax=fig.add_axes([0.125, 0.1, 0.8, 0.8])
    thread.start_new_thread(drawRecords, ("DrawRecords",0.02))    
    serve_forever()
   ###
    plt.show()
###

