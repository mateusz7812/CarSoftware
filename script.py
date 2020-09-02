import time

import RPi.GPIO as GPIO

import xbox

ENGINE_IN1 = 10
ENGINE_IN2 = 9
ENGINE_PWM = 11
SERVO_PWM = 17

HIGH = GPIO.HIGH
LOW = GPIO.LOW

GPIO.setmode(GPIO.BCM)

GPIO.setup(ENGINE_IN1, GPIO.OUT)
GPIO.setup(ENGINE_IN2, GPIO.OUT)
GPIO.setup(ENGINE_PWM, GPIO.OUT)
GPIO.setup(SERVO_PWM, GPIO.OUT)

def update_engine(engine):
    value = joy.leftY()

    print("y: {}".format(value))

    duty_cycle = value * 100
    engine_in1 = LOW
    engine_in2 = LOW

    if value > 0:
        engine_in1 = HIGH

    elif value < 0:
        engine_in2 = HIGH
        duty_cycle = duty_cycle * -1

    engine.ChangeDutyCycle(duty_cycle)
    GPIO.output(ENGINE_IN1, engine_in1)
    GPIO.output(ENGINE_IN2, engine_in2)


def update_servo(servo):
    value = joy.leftX()
    pwm_value = 6.5 - (3 * value)
    servo.ChangeDutyCycle(pwm_value)
    print("x: {}, pwm: {}".format(value, pwm_value))


if __name__ == '__main__':
    joy = xbox.Joystick(10)

    engine_handler = GPIO.PWM(ENGINE_PWM, 100)
    engine_handler.start(0)

    servo_handler = GPIO.PWM(SERVO_PWM, 50)
    servo_handler.start(6)

    while not joy.Back():
        update_engine(engine_handler)
        update_servo(servo_handler)
        time.sleep(0.1)

    joy.close()

    engine_handler.stop()
    servo_handler.stop()

    GPIO.cleanup()
