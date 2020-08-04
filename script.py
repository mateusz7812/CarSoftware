

import RPi.GPIO as GPIO
import xbox
import time

AIN1 = 2
AIN2 = 3
PWMA = 4

HIGH = GPIO.HIGH
LOW = GPIO.LOW

GPIO.setmode(GPIO.BCM)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
import RPi.GPIO as GPIO
import xbox
import time

AIN1 = 2
AIN2 = 3
PWMA = 4

HIGH = GPIO.HIGH
LOW = GPIO.LOW

GPIO.setmode(GPIO.BCM)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)


def setAIN(ain1, ain2):
    GPIO.output(AIN1, ain1)
    GPIO.output(AIN2, ain2)


def setPWM(pwm, value):
    pwm.ChangeDutyCycle(value * 100)


if __name__ == '__main__':
    joy = xbox.Joystick(10)
    pwm = GPIO.PWM(PWMA, 100)
    pwm.start(0)

    while not joy.Back():
        value = joy.leftY()

        if value == 0:
            setAIN(LOW, LOW)
        elif value > 0:
            setAIN(HIGH, LOW)
	    setPWM(pwm, value)
        else:
            setAIN(LOW, HIGH)
            setPWM(pwm, value * (-1))
	print(value)
	time.sleep(0.1)

    joy.close()
    pwm.stop()
