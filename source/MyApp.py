import cv2
from flask import Flask, render_template, request
import camera
import circuit
import Adafruit_MCP3008
app = Flask(__name__)
camera.init(width=320, height=240)

if not camera.camera.isOpened():
    print("Camera is not opened.")
else:
    print("Camera successfully opened.")

@app.route('/')
def index():
        temperature = circuit.getTemperature(circuit.sensor)
        humidity = circuit.getHumidity(circuit.sensor)
        light = circuit.getLight()
        distance = circuit.measure_distance()
        return render_template("MyHtml.html",temperature=temperature, humidity=humidity, light=light, distance = distance)
@app.route('/cctv')
def cctv():
    # 카메라로부터 이미지 캡처
    image = camera.take_picture(most_recent=True)
    if image is not None:
        # 이미지 저장
        cv2.imwrite('./static/cctv.jpg', image)
        # 이미지 경로를 템플릿에 전달
        return render_template("cctv.html", fname='./static/cctv.jpg')
    else:
        # 이미지 캡처 실패 시 메시지 표시
        return render_template("cctv.html", fname=None)

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080, debug=True)