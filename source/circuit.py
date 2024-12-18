import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio
import Adafruit_MCP3008
import cv2
import threading
camera = None

# LED를 켜고 끄는 함수
def controlLED(on_off): # led 번호의 핀에 on_off(0/1) 값 출력하는 함수
        global led
        GPIO.output(led, on_off)

# 초음파 센서를 제어하여 물체와의 거리를 측정하여 거리 값 리턴하는 함수
def measure_distance():
        global trig, echo
        time.sleep(0.2) # 초음파 센서의 준비 시간을 위해 200밀리초 지연
        GPIO.output(trig, 1) # trig 핀에 1(High) 출력
        GPIO.output(trig, 0) # trig 핀에 0(Low) 출력. High->Low. 초음파 발사 지시

        while(GPIO.input(echo) == 0): # echo 핀 값이 0->1로 바뀔 때까지 루프
                pass

        # echo 핀 값이 1이면 초음파가 발사되었음
        pulse_start = time.time() # 초음파 발사 시간 기록
        while(GPIO.input(echo) == 1): # echo 핀 값이 1->0으로 바뀔 때까지 루프
                pass

        # echo 핀 값이 0이 되면 초음파 수신하였음
        pulse_end = time.time() # 초음파가 되돌아 온 시간 기록
        pulse_duration = pulse_end - pulse_start # 경과 시간 계산
        return pulse_duration*340*100/2 # 거리 계산하여 리턴(단위 cm)

def getTemperature(sensor) : # 센서로부터 온도 값 수신 함수
        return float(sensor.temperature) # HTU21D 장치로부터 온도 값 읽기

def getHumidity(sensor) : # 센서로부터 습도 값 수신 함수
        return float(sensor.relative_humidity) # HTU21D 장치로부터 습도 값 읽기

def getLight():
                return mcp.read_adc(0)

#모터 제어 함수
#모터를 duration초간 돌리고 정지

def activateMotor(INA,INB,EN,stat,duration=1):
        if stat == FORWARD:#앞으로 돌림
                        GPIO.output(INA,1)
                        GPIO.output(INB,0)
                        GPIO.output(EN,1)
                        time.sleep(duration)
                        GPIO.output(INA,0)
                        GPIO.output(INB,0)
                        GPIO.output(EN, 0)
        elif stat == BACK:#반대로 돌림
                        GPIO.output(INA,0)
                        GPIO.output(INB,1)
                        GPIO.output(EN, 1)
                        time.sleep(duration)
                        GPIO.output(INA,0)
                        GPIO.output(INB,0)
                        GPIO.output(EN, 1)

def controlMotor(stat):
        global motorFlag
        if stat == 1 and motorFlag!=1:#모터 3개 모두 앞으로
                activateMotor(IN1,IN2,19,1)
                motorFlag = 1

        elif stat == 2 and motorFlag != 0:#모터 3개 모두 뒤로
                activateMotor(IN1,IN2,19,2,0.1)
                motorFlag = 0
        else:#모터 3개 모두 정지
                activateMotor(IN1,IN2,19,0)

# 초음파 센서를 다루기 위한 전역 변수 선언 및 초기화
trig = 20 # GPIO20
echo = 16 # GPIO16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT) # GPIO20 핀을 출력으로 지정
GPIO.setup(echo, GPIO.IN) # GPIO16 핀을 입력으로 지정

# LED를 다루기 위한 전역 변수 선언 및 초기화
led = 5 # GPIO6
GPIO.setup(led, GPIO.OUT) # GPIO6 핀을 출력으로 지정

# 온습도 센서를 다루기 위한 전역 변수 선언 및 초기화
sda = 2 # GPIO2 핀. sda 이름이 붙여진 핀
scl = 3 # GPIO3 핀. scl 이름이 붙여진 핀
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)

# 조도 센서를 다루기 위한 전역변수 선언 및 초기화
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

#모터를 다루기 위한 전역변수 선언 및 초기화
#모터 채널
CH1 = 0
CH2 = 1
#GPIO PIN
#모터 1
IN1 = 6
IN2 = 13
EN1 = 19

#방향
FORWARD = 1
BACK = 2
STOP = 0

motorFlag = 0
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN1, GPIO.OUT)
