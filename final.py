from pyzbar import pyzbar
from datetime import datetime
import argparse
import cv2
import sys
import time
import RPi.GPIO as GPIO

#test0

servo_max_duty = 12
servo_min_duty = 3

GPIO.setmode(GPIO.BOARD)
button_pin = 37
motor_pin = 35
motor_pin2a = 31
motor_pin2b = 29

GPIO.setup(motor_pin2a, GPIO.OUT)
GPIO.setup(motor_pin2b, GPIO.OUT)

GPIO.setup(button_pin , GPIO.IN)
GPIO.setup(motor_pin, GPIO.OUT)
start2 = 0
servo = GPIO.PWM(motor_pin, 50)
servo.start(0)           
vc = cv2.VideoCapture(0)
GPIO.output(motor_pin2a,True)
GPIO.output(motor_pin2b,False)



def setangle(degree):
    if degree > 180:
        degree = 180

    duty = servo_min_duty + (degree * (servo_max_duty - servo_min_duty) / 180)
    servo.ChangeDutyCycle(duty)


while True :
    #time.sleep(0.1)
    print("waiting...")
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if start2 > 0 and time.time() - start2 > 30:    
        #servo.start(0) 
        setangle(0)
        start2 = 0

        motorstart = time.time()
                while time.time()-motorstart <= 3:
                     GPIO.output(motor_pin2a,False)
                         GPIO.output(motor_pin2b,True)

        break       

    if GPIO.input(button_pin) == False:
        print("webcam start!")
        start = time.time()
        chk = 0
                    
        vc.set(10,0.5)


        while time.time() - start <= 90 :

            ret, frame = vc.read()
            cv2.imshow("Video Window", frame)   
            cv2.imwrite('image.jpg',frame)     

            #ap.add_argument("-i","--image", required = True, help = "path to input image")
            #ap = argparse.ArgumentParser()
            #args = vars(ap.parse_args())

            image = cv2.imread('image.jpg')
            barcodes = pyzbar.decode(image)

            if barcodes:
                break
                chk = 1
                    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            
        vc.release()
        cv2.destroyAllWindows()

        if chk == 1:
            print("access success")

        else:
            print("access failed")

        """
        #test1
        ap = argparse.ArgumentParser()
        args = vars(ap.parse_args())

        image = cv2.imread(args["image"])
        barcodes = pyzbar.decode(image)
        """

        for barcode in barcodes:

            (x,y,w,h) = barcode.rect
            cv2.rectangle(image, (x,y) , (x+w , y + h), (0,0,255) ,2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            #text = "{} ({})".format(barcodeData, barcodeType)
            #cv2.putText(image, text, (x,y - 10) , cv2.FONT_HERSHEY_SIMPLEX,0.5 , (0,0,255),2)

            #print("[INFO' Found {} barcode:{}".format(barcodeType, barcodeData))

            cv2.imshow("image", image)
            #cv2.waitKey(0)

            #file string #string1 txt data
            data =  open('data2.txt', 'a')
            print(str(time.time() - start) + "time file is going")    
            text2 = datetime.now().strftime("%m/%d/%Y, %H:%M:%S ") +  barcodeData.encode("utf-8") + '\n'
            data.write(text2)       
            data.close()

            #opening door
            #servo.start(0) 
            setangle(90)
            start2 = time.time()
        
            motorstart = time.time()
            while time.time()-motorstart <= 3:
                GPIO.output(motor_pin2a,True)
                GPIO.output(motor_pin2b,False)
            

