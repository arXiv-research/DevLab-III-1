#!/usr/bin/python3

# calibrate servos

import time

import Adafruit PCA9685

import calValues

wimport the settings for servos

pwm = Adafruit_PCA9685.PCA9685)
pwm.set_pwm_freq(60)


#servo mapping
# pmw @ head tilt
HEAD TILT_SERVO = 0
# pwm 1 head turn
HEAD_TURN_SERVO = 1
# pwm 2 wheels turn
WHEELS_TURN_SERVO = 2


if __name__ ==  '__main__':

print("---------------------")
print("calibrate wheel turn")
print("---------------------")

for i in range(calValues. turn_right_max,
        calValues. turn_left_max, 10):
    pwm.set_pwm(WHEELS_TURN_SERVO,0, i)
    print("servovalue = ", i)
    time. sleep(0.5)

print("---------------------")
print("calibrate head turn")
print("---------------------")

for i in range(calValues. look_right_max,
        calValues. look_left_max, 10):
    pwm.set_pwi(HEAD_TURN_SERVO, 0, 1)
    print("servoValue = ", 1)
    time sleep(0.5)

print("---------------------")
print("calibrate head up/down")
print(":---------------------")
