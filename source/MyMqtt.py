
import time
import paho.mqtt.client as mqtt
import circuit
import json

def on_connect(client, userdata, flag, rc, prop=None):
        client.subscribe("led") # "led" 토픽으로 구독 신청
        client.subscribe("motor")# "motor" 토픽으로 구독 신청

def on_message(client, userdata, msg) :
        print(f"토픽: {msg.topic}, 페이로드: {msg.payload}")
        topic = msg.topic
        payload = int(msg.payload)

        if topic == "led":
                print(topic, " ", payload)
                circuit.controlLED(payload) # LED를 켜거나 끔
                print(f"LED 상태 변경: {'켜짐' if payload else '꺼짐'}")
        elif topic == "motor":
              print(topic, " ", payload)
              if payload == 2:
                    print("모터 가동 중")
                    circuit.controlMotor(circuit.BACK)
              else:
                    print("Unknown motor command received")
        elif topic == "beat":
              print("맴매 on/off")
              circuit.activateBeat(23,24,18,payload)
        else:
              print("Unknown topic")
        circuit.controlLED(0)

ip = "localhost" # 현재 브로커는 이 컴퓨터에 설치되어 있음

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(ip, 1883) # 브로커에 연결
client.loop_start() # 메시지 루프를 실행하는 스레드 생성

# 도착하는 메시지는 on_message() 함수에 의해 처리되어 LED를 켜거나 끄는 작업과
# 병렬적으로 1초 단위로 초음파 센서로부터 거리를 읽어 전송하는 무한 루프 실행
while True:
    temp = circuit.getTemperature(circuit.sensor)
    humidity = circuit.getHumidity(circuit.sensor)
    distance = circuit.measure_distance()  # 초음파 센서로부터 거리 읽기
    light = circuit.getLight()

    if distance < 3 and temp >= 20 and temp < 26 and humidity >= 40 and humidity <=70 and light < 300:
       print("Motor is activating")
       circuit.controlMotor(circuit.FORWARD)
       circuit.controlLED(1)
       time.sleep(3)
    elif circuit.motorFlag == 1:
          continue



    # 데이터를 JSON 형태로 패키징

    # "ultrasonic" 토픽으로 데이터 전송 (JSON 문자열로 변환)
    # client.publish("ultrasonic", json.dumps(data))
    time.sleep(1)  # 1초 동안 잠자기

client.loop_stop() # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
