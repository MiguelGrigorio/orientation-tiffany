from is_wire.core import Subscription
from is_msgs.image_pb2 import Image
import time
from utils.code.classes.StreamChannel import StreamChannel
import cv2
from utils.code.functions.toNumpy import toNumpy

def getImages(path_images: str, qntImages: int, cameraList: list, show: bool = False) -> None:
    for cameraNumber in cameraList:
        print('---RUNNING CAMERA {} CLIENT---'.format(cameraNumber))

        broker_uri = "amqp://guest:guest@10.10.2.211:30000"

        channel_1 = StreamChannel(broker_uri)

        subscription_1 = Subscription(channel = channel_1)
        subscription_1.subscribe(topic = 'CameraGateway.{}.Frame'.format(cameraNumber))

        window_1 = f'Intelbras Camera {cameraNumber}'

        i = 1
        time_1 = time.time()

        while i <= qntImages:

            msg = channel_1.consume_last()  
            if type(msg) != bool: 
                im_1 = msg.unpack(Image)
                frame_1 = toNumpy(im_1)

            if show:
                cv2.imshow(window_1, frame_1)

            #print(time.time() - time_1)

            if qntImages > 1:
                name = f"camera{cameraNumber}_{i}.jpg"
            else:
                name = f"camera{cameraNumber}.jpg"

            if time.time() - time_1 > 1:
                time_1 = time.time()
                cv2.imwrite(f"{path_images}" + name, frame_1)
                i+=1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break