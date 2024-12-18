import cv2
from flask import Flask, render_template
import camera # 카메라 모듈, camera.py 임포트
app = Flask(__name__) # 플라스크 객체 생성
camera.init(width=320, height=240) # 카메라 모듈 초기화

@app.route('/cctv')
def cctv( ):
        image = camera.take_picture(most_recent=True) # 사진 촬영. 이미지 읽기
        if image is not None:
                cv2.imwrite('./static/cctv.jpg', image) # 이미지를 ./static 디렉터리에 파일로 저장

                # file_name를 사용하여 cctv.html를 변경하고, 파일 텍스트를 문자>열로 리턴
                return render_template("cctv.html", fname='/static/cctv.jpg')
        else:
        # 이미지 캡처 실패 시 메시지 표시
                return render_template("cctv.html", fname=None)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080) # debug=True 속성을 사용하면 오류 발생
