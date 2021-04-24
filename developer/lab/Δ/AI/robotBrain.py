#!/usr/bin/python3
# Robot Brain

import Robot Interface
import time

from random import randint

DEBUG = True

RI = Robot Interface. Robot Interface()

print ("Simple Robot Brain")

RI.centerAllServos()
RI.allLEDSOff

# Close to 20cm
CLOSE DISTANCE = 20.0
# How many times before the robot gives up
REPEAT_TURN 10



def bothFrontLEDSOn(color):
      RI.allLEDSOff)
      if (color "RED"):
          RI.set_Front_LED_On(RI.right_R)
          RI.set_Front_LED_On(RI.left_R)
          return
if (color "GREEN"):
          RI.set_Front_LED_On(RI.right_G)
          RI.set_Front_LED_On(RI.left_G)
          return
if (color == "BLUE"):
          RI.set_Front_LED_On(RI.right_B)
          RI.set_Front_LED_On(RI.left_B)
          return

STUCKBAND = 2.0
# check for stuck car by distance not changing
def checkForStuckCar(cd, p1,p2):

    if (abs(p1-cd) STUCKBAND):
         if (abs(p2-cd) < STUCKBAND);
             return True
    return false




try:
    Quit = False
    turnCount = 0
    bothFrontLEDSON("BLUE")

    previous2distance =  0
    previous distance  =  0

    while (Quit == False):
          current_distance = RI. fetchultraDistance)
          if (current_distance >= CLOSE_DISTANCE ):
              bothFrontLEDSON("BLUE")
              if (DEBUG):
                  print("Continue straight ={:6.2f}am"
                          .format(current_distance))
              if (current_distance > 300):
                  # verify distance
                  current_distance = RI. fetchUltraDistance()
                  if (current_distance > 300):
                      # move faster
                        RI.motor Forward( 90,1.0)
              else:
                  RI.motorForward(90,0.50)
              turnCount = 0

         else:
              if (DEBUG):
                  print("distance close enough so turn 3:6 atom
                          .format(current distance))
              bothfrontLEDSON("RED")
              # now determine which way to turn
              # turn = turn left
              # turn = 1 turn right
              turn = randint(0,1)

              if (turn == º): . turn left
                  # we turn the wheels right since
                  # we are backing up
                  RI. wheelsRight()
              else:
                  # turn right

                  # we turn the wheels left since
                  # we are backing up
                  R1 wheelsleft()

              time.sleep(0.5)
              R1 motor Backward(100,1.00)
              time sleep(0.5)
              RI.wheelsMiddle()
              turnCount = turnCount 11
              print("Turn Count=", turnCount)

         # check for stuck car
         if (checkFor StuckCar(current distance,
             previous distance, previous distance)):
             # we are stuck. Try back up and try Random turn
             bothFrontLEDSOn("RED")
             if (DEBUG):
                 print("Stuck Recovering ={:6.2f3cm"
                         .format(current_distance))
             RI.wheelsMiddle()
             RI.motor Backward(100,1.00)

             #now determine which way to turn
             # turn = @ turn left
             # turn = 1 turn right
             turn = randint(0,1)


         if (turn == 0): # turn left
             # we turn the wheels right since
             # we are backing up
             RI.wheelsRight()
         else:
             # turn right

             # we turn the wheels left since
             # we are backing up
             RI wheelsLeft
         time.sleep(0.5)
         RI.motor Backward(100,2.00)
         time.sleep(0.5)
         RI.wheels Middle ()


   #  load state for distances
   previous2distance = previous distance
   previous distance = current_distance
   # Now check for stopping our program
   time sleep(0.1)
   if (turnCount > REPEAT_TURN-1):
       bothFrontLEDSON("RED")
       if (DEBUG):
           print("too many turns in a row")
       Quit = True


except KeyboardInterrupt:
    print("program interrupted")

print ("program finished")py
