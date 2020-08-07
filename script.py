import time

import RPi.GPIO as GPIO

import xbox

AIN1 = 2
AIN2 = 3
ENGINE_PWM = 4
SERVO_PWM = 17
STBY = 10
VMOT = 10

HIGH = GPIO.HIGH
LOW = GPIO.LOW

GPIO.setmode(GPIO.BCM)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(ENGINE_PWM, GPIO.OUT)
GPIO.setup(SERVO_PWM, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(VMOT, GPIO.OUT)


def setAIN(ain1, ain2):
    GPIO.output(AIN1, ain1)
    GPIO.output(AIN2, ain2)


def setPWM(handler, value):
    handler.ChangeDutyCycle(value * 100)


def update_engine(engine):
    value = joy.leftY()
    if value == 0:
        setAIN(LOW, LOW)
    elif value > 0:
        setAIN(HIGH, LOW)
        setPWM(engine, value)
    else:
        setAIN(LOW, HIGH)
        setPWM(engine, value * (-1))
    print("y: " + value)


def update_servo(servo):
    value = joy.leftX()
    pwm_value = (3 * value) + 6
    servo.ChangeDutyCycle(pwm_value)
    print("x:" + value)


def setup_driver():
    GPIO.output(VMOT, HIGH)
    time.sleep(1)
    GPIO.output(STBY, HIGH)
    time.sleep(1)


def teardown_driver():
    time.sleep(1)
    GPIO.output(STBY, LOW)
    time.sleep(1)
    GPIO.output(VMOT, LOW)


if __name__ == '__main__':
    setup_driver()

    joy = xbox.Joystick(10)

    engine_handler = GPIO.PWM(ENGINE_PWM, 100)
    engine_handler.start(0)

    servo_handler = GPIO.PWM(SERVO_PWM, 100)
    servo_handler.start(6)

    while not joy.Back():
        update_engine(engine_handler)
        update_servo(servo_handler)
        time.sleep(0.1)

    joy.close()

    engine_handler.stop()
    servo_handler.stop()

    GPIO.cleanup()

    teardown_driver()