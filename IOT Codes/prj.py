from flask import Flask,render_template,request,jsonify,redirect,url_for
import RPi.GPIO as GPIO
import time
app=Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
st1=11
st2=12
st3=13
st4=15
ser1=18
ser2=35
buzz=21
fWaitTime = 0.002
aMotorPins = [12,15,11,13]
aSequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
GPIO.setup(ser1,GPIO.OUT)
GPIO.setup(ser2,GPIO.OUT)
GPIO.setup(st1,GPIO.OUT)
GPIO.setup(st2,GPIO.OUT)
GPIO.setup(st3,GPIO.OUT)
GPIO.setup(st4,GPIO.OUT)
GPIO.output( st1, GPIO.LOW )
GPIO.output( st2, GPIO.LOW )
GPIO.output( st3, GPIO.LOW )
GPIO.output( st4, GPIO.LOW )
GPIO.setup(buzz,GPIO.HIGH)
pwm_servo1=GPIO.PWM(ser1,50)
pwm_servo2=GPIO.PWM(ser2,50)
pwm_servo1.start(0)
pwm_servo2.start(12.5)

global m1,tu1,w1,th1,fr1,sa1
m1,tu1,w1,th1,fr1,sa1,su1=0,0,0,0,0,0,0
iNumSteps = len(aSequence)
iDirection = 1
    

@app.route("/",methods=["GET","POST"])
def home():
    if request.method=="POST":
        day=request.form.get('but')
        buzzer()
        motor(day)
        tableup(day)
        return redirect(url_for("home"))
    else:     
        return render_template('index.html')

def buzzer():
        GPIO.setup(buzz,GPIO.OUT)
        GPIO.output(buzz,GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(buzz,GPIO.LOW)
        time.sleep(1)
        GPIO.output(buzz,GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(buzz,GPIO.LOW)
        time.sleep(1)
        GPIO.output(buzz,GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(buzz,GPIO.LOW)
        time.sleep(1)
        GPIO.cleanup(buzz)
        
def motor(day):
    if(day=="mon"):
        ideg=0
    elif(day=="tue"):
        ideg=580
    elif(day=="wed"):
        ideg=1172
    elif(day=="thu"):
        ideg=1752
    elif(day=="fri"):
        ideg=2343
    elif(day=="sat"):
        ideg=2924
    else:
        ideg=3515
    turn(ideg)
  
def turn(iDeg):
    
    iSeqPos=0
    for step in range(0,iDeg):
          for iPin in range(0, 4):
              iRealPin = aMotorPins[iPin]
              if aSequence[iSeqPos][iPin] != 0:
                  GPIO.output(iRealPin, True)
              else:
                  GPIO.output(iRealPin, False)
                  
          iSeqPos += iDirection
          if (iSeqPos >= iNumSteps):
               iSeqPos = 0
          if (iSeqPos < 0):
               iSeqPos = iNumSteps + iDirection
               
          time.sleep(fWaitTime)
    
    time.sleep(1)
    servo()
    rev(iDeg)
          
      
def tableup(day):
    global m1,tu1,w1,th1,fr1,sa1,su1
    if(day=="mon"):
        m1=1
    elif(day=="tue"):
        tu1=1
    elif(day=="wed"):
        w1=1
    elif(day=="thu"):
        th1=1
    elif(day=="fri"):
        fr1=1
    elif(day=="sat"):
        sa1=1
    elif(day=="sun"):
        su1=1
    
def rev(iDeg):
    iDirection=-1
    iSeqPos=0
    for step in range(0,iDeg):
          for iPin in range(0, 4):
              iRealPin = aMotorPins[iPin]
              if aSequence[iSeqPos][iPin] != 0:
                  GPIO.output(iRealPin, True)
              else:
                  GPIO.output(iRealPin, False)
                  
          iSeqPos += iDirection
          if (iSeqPos >= iNumSteps):
               iSeqPos = 0
          if (iSeqPos < 0):
               iSeqPos = iNumSteps + iDirection
               
          time.sleep(fWaitTime)
        
def servo():
    pwm_servo1.ChangeDutyCycle(7.5)
    pwm_servo2.ChangeDutyCycle(7.5)
    time.sleep(1.5)
    pwm_servo1.ChangeDutyCycle(0)
    pwm_servo2.ChangeDutyCycle(12.5)
        
@app.route("/status")
def table():
    global m1,tu1,w1,th1,fr1,sa1,su1
    data=[["Medicine Taken",m1,tu1,w1,th1,fr1,sa1,su1]]
    return render_template('table.html',data=data)
    
if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
