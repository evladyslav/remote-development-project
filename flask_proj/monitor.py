import cv2
from dotenv import load_dotenv
import os 
import serial 
import time 


load_dotenv()

com_port = os.getenv('COM_PORT')
port_baudrate = os.getenv('PORT_BAUDRATE')


class SerialPort:
    def __init__(self, port, baudrate=port_baudrate, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_port = None

    def __enter__(self):
        self.serial_port = serial.Serial(
            self.port, self.baudrate, timeout=self.timeout
        )
        return self

    def __exit__(self, *exc):
        if self.serial_port:
            self.serial_port.close()

    def read_code(self):
        while True:
            data = self.serial_port.readline().decode('utf-8')
            if data: 
                yield f"{data}"

                
def generate_serial_data():
    with SerialPort(com_port, baudrate=port_baudrate) as ser:
        for data in ser.read_code():
            if data.strip():
                yield f'data: {data.strip()}\n\n'
                time.sleep(0.1)  


def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()


