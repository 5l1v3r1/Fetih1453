#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque
import numpy as np
import argparse
import cv2
import time
import sys
import RPi.GPIO as GPIO
import imutils


mode=GPIO.getmode()

GPIO.cleanup()

motor1=24
motor2 = 23
motor3=22
motor4 = 21

sleeptime=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor1, GPIO.OUT)
GPIO.setup(motor2, GPIO.OUT)
GPIO.setup(motor3, GPIO.OUT)
GPIO.setup(motor4, GPIO.OUT)

def forward(x):
GPIO.output(motor1, GPIO.HIGH)
GPIO.output(motor2, GPIO.HIGH)
time.sleep(x)
GPIO.output(Forward, GPIO.LOW)
GPIO.output(Forward, GPIO.LOW)

def sag(x):
GPIO.output(motor3, GPIO.HIGH)
time.sleep(x)
GPIO.output(motor3, GPIO.LOW)

def sol(x):
GPIO.output(motor4, GPIO.HIGH)
time.sleep(x)
GPIO.output(motor4, GPIO.LOW)


x = 0 #programın ileride hata vermemesi için x 0 olarak tanımlıyorum
y = 0 # programın ileride hata vermemesi için y 0 olarak tanımlıyorum
r = 0
cap = cv2.VideoCapture(0) # webcamin bagli oldugu port varsayilan 0 

ret, frame = cap.read() # kameradan gelen görüntülerin alınması

#sari rengin algilanmasi
colorLower = (24, 100, 100) 
colorUpper = (44, 255, 255)
#converter.py ile convert ettiğiniz rengi buraya giriniz
camera = cv2.VideoCapture(0) # kameradan 
while True: #yazılımımız çalıştığı sürece aşağıdaki işlemleri tekrarla

    
     (grabbed, frame) = camera.read() # grabbed ve frame değişkenini camera.read olarak tanımlıyoruz.

     frame = imutils.resize(frame, width=600) # görüntü genişliğini 600p yapıyoruz

     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # görüntüyü hsv formatına çeviriyoruz
 
    
     mask = cv2.inRange(hsv, colorLower, colorUpper) # hsv formatına dönen görüntünün bizim belirttiğimiz renk sınırları içerisinde olanları belirliyor
     mask = cv2.erode(mask, None, iterations=2) # bizim renklerimizi işaretliyor
     mask = cv2.dilate(mask, None, iterations=2) # bizim renklerimizin genişliğini alıyor
    
    
     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
     cv2.CHAIN_APPROX_SIMPLE)[-2]
     center = None
 

     if len(cnts) > 0:

             c = max(cnts, key=cv2.contourArea)
             ((x, y), radius) = cv2.minEnclosingCircle(c)
             M = cv2.moments(c)
             center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        
             if radius > 10: #algılanacak hedefin minumum boyutu
                 cv2.circle(frame, (int(x), int(y)), int(radius),
                 (0, 255, 255), 2)
                 cv2.circle(frame, center, 5, (0, 0, 255), -1)
     print("x : ")
     print(x) # kameradan gelen görüntüde bizim rengimiz varsa x kordinatı
     print("y : ")
     print(y) # kameradan gelen görüntüde bizim rengimiz varsa y kordinatı
     print("r : ")
     print(r) # kameradan gelen görüntüde bizim rengimiz varsa y kordinatı
     if (x == 0 and y == 0): #hedef algilanmadiysa
         sag(5)
         GPIO.cleanup()
         print("hedef algilanmadi kendi etrafimda dönüyorum...")
     
     elif (x > 360 and x < 390 and y > 240 and y < 270 ): # hedef ortadaysa
         forward(5)
         GPIO.cleanup()
         print("Düz Gidiliyor...")

     elif (x < 360): # hedef robotun solunda kalıyorsa
          sol(5) # sola dön komutun kontrol edilmesi lazım
          GPIO.cleanup()
          print("Sol'a dönülüyor...")
          
     elif (x > 390): # hedef robotun saginda kaliyorsa
         sag(5)
         GPIO.cleanup()
         print("Sag'a dönülüyor...")
