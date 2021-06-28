#!/usr/bin/env python
# Author:      Niels Affourtit
#
# Created:     01-02-2015
# Copyright:   (c) Niels 2015
# Licence:     <your licence>
# TODO: heartbeat for fail safe. Feedback via website (lights on/off etc)
# pull umbilical and stop motor
#-------------------------------------------------------------------------------
import win32api #to capture keyboard even out of focus
import socket
import pygame
import time
import datetime
# Setup pygame and key states
global DriveCommands
global Command
##global fps
global moveLeft
global moveRighte
global moveQuit
hadEvent = True
 
fps             = 5                   # Quantity read Joystick  per second (def 20 times per second)
 
broadcastIP = '192.168.1.23'           # IP address to send to, 255 in one or more positions is a broadcast / wild-card
#broadcastIP = '192.168.178.35'          # raspberry 1B+
#broadcastIP = 'raspberryipi'
#broadcastIP = '192.168.178.29'          # raspberry 2
broadcastPort = 5000                    # What message number to send with
 
# values will be send in list. Item in list explained below:
MotorPort1 = 0                          # Drive number for left motor
MotorStar2 = 1                          # Drive number for right motor
MotorVert3 = 2                          # Drive number for vertical motor
tilt       = 0.16                         # initialize tilt of webcam
Lights     = 0                          # toggle lights on or off.
## Joystick INPUT settings
regularUpdate   = True                  # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released
AxesForward     = 0
AxesSide        = 1
AxesThrottle    = 2                     # regulate up down speed.
DurationmSec    = 0
##ButtonDescend   = 0
##ButtonAscend    = 1
##ButtonTiltUp    = 2
##ButtonTiltDown  = 3
##ButtonLights    = 4                     # after 0.5s turn on/off lights
##ButtonRecordStart= 5                    # after 0.5s Start recording
##ButtonRecordStop= 6                     # after 0.5s Stop recording
##Button_Quit     = 7                    # quit python script
##ButtonCalESC    = 8                     # Keep pressed for 5 seconds to start calibration routine ESC Turn off ESC, full throttle, startup ESC etc)
ServoMax    = [0.245,0.245,0.245,0.185,0.245,0.245] #limit sweep on some servos
ServoMin    = [0.055,0.055,0.055,0.13195,0.055,0.055]
 
 
# Tilt                                  # Tilt parameter down0-10up for webcam
DriveCommands   = [0.15,0.15,0.15,0.15,'x','x',1]
AxisInvert      = [1,-1,-1]              #invert axis 3
AxisAdjust      = [0.008,0.008,0]
Command=""
# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # Create the socket
##sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
##sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)
#sender.sendto("JoystickSendPC1 activated.", (broadcastIP, broadcastPort))                # hello world
 
def isKeyPressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    return (win32api.GetKeyState(key) & (1 << 7)) != 0
 
 
 
pygame.init()
 
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Initialize the joysticks
pygame.joystick.init()
#pygame.event.set_grab()
power=1.0
 
# Get ready to #print
##text#print = Text#print()
buttonPressed=0
##when_pressed=0.0
# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            #print "Joystick button pressed."
            if buttonPressed <> 1:
                when_pressed = datetime.datetime.now()
            buttonPressed=1
        if event.type == pygame.JOYBUTTONUP:
            buttonPressed=0
 
 
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
 
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
 a
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        #print "Joystick name: %s" % name
 
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()       #3 axis
        #print axes
 
        for i in range( axes ):
            axis = joystick.get_axis( i )*AxisInvert[i]+AxisAdjust[i]
            if abs(axis)<0.03: axis=0.00
            #print "Axes number is %i" % axis
            DriveCommands[i]=round(axis,2)            # fill list with values
        VertThrustAbs=round((DriveCommands[2]+ 1)/2,2)   #Vertical absolute value between 1 and 0
        DriveCommands[2]=0
        buttons = joystick.get_numbuttons()
        #print "number of buttons %i)" % buttons
 
        for i in range( buttons ):
            if buttonPressed ==1:
                Duration=(datetime.datetime.now()-when_pressed)
                DurationmSec=int(Duration.total_seconds()*1000)
            else:
                DurationmSec=0
##            print DurationmSec
            button = joystick.get_button( i )
            if i == 0 and button == 1:
                DriveCommands[2] = VertThrustAbs  #while pressed UP power according to lever
                Command =""  #cancel auto depth/height
            if i == 1 and button == 1:
                DriveCommands[2] = -VertThrustAbs #while pressed Down power according to lever
                Command ="" #cancel auto depth/height
            if i == 2 and button == 1:
                if tilt < 1.0: tilt = tilt +0.25/fps
##                print "Button nr %i value %f with value %f " %(i,button,tilt)
                hadEvent = True
            if i == 3 and button == 1:
                if tilt > -1.0: tilt = tilt -0.25/fps
                hadEvent = True
##                print "Button nr %i value %f with value %f " %(i,button,tilt)
            if i == 4 and button == 1:  #lights
                if DurationmSec > 100:
##                print when_pressed
                    if Lights == 1 : Lights=0  # 1=ON
                    else: Lights = 1
##                    print 'Lights are turned : %i' % Lights
                    buttonPressed=0
            if i == 5 and button == 1:      #stop/start keeping height above seabed
                if DurationmSec > 200:
                    if Command == "Height" : Command=""  # 1=ON
                    else: Command='Height'
##                    print 'Stream recording turned ON ( %s )' %Command
                    buttonPressed=0
            if i == 6 and button == 1:      #stop/start keeping depth
                if DurationmSec > 200:
                    if Command == "Depth" : Command=""  # 1=ON
                    else: Command='Depth'
                    buttonPressed=0
            if i == 7 and button == 1:
                if DurationmSec > 500:
                    sender.sendto("Bye", (broadcastIP, broadcastPort))
                    print "Button 8 is pressed, server terminated"
                    quit()               #stop script
        for i in range(0,4): #keep values within allowable
            if DriveCommands[i] <-1.0 : DriveCommands[i]=-1.0
            elif DriveCommands[i] >1.0: DriveCommands[i]=1.0
        M1=DriveCommands[1]+DriveCommands[0]          # Convert forward-side to lef and right
        M2=DriveCommands[1]-DriveCommands[0]         # motor.
        if M1 >1:M1=1.0
        elif M1 < -1.0: M1=-1.0
        if M2 >1 :M2=1
        elif M2 < -1.0: M2=-1.0
        DriveCommands[0]=M1                      # overwrite original array (ugly way)
        DriveCommands[1]=M2
        for ID in range(0,4):
            PulseNeu=(ServoMax[ID]+ServoMin[ID])/2  #0.150 0.95 range=PulsePos
            PulseNeg=PulseNeu-ServoMin[ID]      # width above 0 0.095
            PulsePos=ServoMax[ID]-PulseNeu      # width below 0
    ##            print PulsePos,PulseNeu,PulseNeg
            if DriveCommands[ID]>0.0 : pulse=DriveCommands[ID]*PulsePos+PulseNeu
            else: pulse=DriveCommands[ID]*PulseNeg+PulseNeu         # axis already <= 1 max.
    ##            print "pulse of servo %i is %f " % (ID,pulse)
            DriveCommands[ID]=pulse
 
    if isKeyPressed(0x25):  #left
                DriveCommands[0]=0.15  #left motor stop
                DriveCommands[1]=0.15+0.095*power  #right motor forward
    elif isKeyPressed(0x26): #up
                DriveCommands[0]=0.15+0.095*power  #left motor forward
                DriveCommands[1]=0.15+0.095*power  #right motor forward
    elif isKeyPressed(0x27): #right
                DriveCommands[0]=0.15+0.095*power  #left motor forward
                DriveCommands[1]=0.15  #right motor stop
    elif isKeyPressed(0x28): #down
                DriveCommands[0]=0.15-0.095*power  #left motor back
                DriveCommands[1]=0.15-0.095*power  #right motor back
    elif isKeyPressed(0xA0): #left shift (up)
                DriveCommands[2] = 0.245
    elif isKeyPressed(0xA2): #left ctrl (down)
                DriveCommands[2] = 0.055
    elif isKeyPressed(ord('L')): #light on/off
                if Lights == 1 : Lights=0  # 1=ON
                else: Lights = 1
                pygame.time.wait(400)# wait 0.1 seconds to avoid on-off-on flash
    elif isKeyPressed(ord('1')): power=0.3#power low
    elif isKeyPressed(ord('2')): power=0.6#power medium
    elif isKeyPressed(ord('3')): power=1.0 #power high
    elif isKeyPressed(ord('H')): #auto height on/off               
                    if Command == "Height" : Command=""  # 1=ON
                    else: Command='Height'
                    pygame.time.wait(400)
    elif isKeyPressed(ord('D')): #auto Depth on/off 
                    if Command == "Depth" : Command=""  # 1=ON
                    else: Command='Depth'
                    
                    pygame.time.wait(400)
 
 
 
    now= (datetime.datetime.now())
#        timecode=now.hour*3600+now.minute*60+now.second+int(now.microsecond/100000)/10.0
 
 
 
    DriveCommands[3]=round(tilt,2)
    DriveCommands[4]=Command                #commands button only one simultaneously
    DriveCommands[5]=Lights
    DriveCommands[6]=now
    for i in range(0,7):
        DriveCommands[i]=str(DriveCommands[i])
    print DriveCommands
    sender.sendto(','.join(DriveCommands), (broadcastIP, broadcastPort))
    for i in range(3): #reset drivecommands
            DriveCommands[i]="0.15"
 
 
    # Limit to 4 frames per second
    clock.tick(fps)
 
 
 
pygame.quit ()
