from is_wire.core import Channel,Subscription,Message
from is_msgs.image_pb2 import Image
import time
from utils.code.streamChannel import StreamChannel
import numpy as np
import cv2

def to_np(input_image):
    if isinstance(input_image, np.ndarray):
        output_image = input_image
    elif isinstance(input_image, Image):
        buffer = np.frombuffer(input_image.data, dtype=np.uint8)
        output_image = cv2.imdecode(buffer, flags=cv2.IMREAD_COLOR)
    else:
        output_image = np.array([], dtype=np.uint8)
    return output_image

def to_image(input_image, encode_format='.jpeg', compression_level=0.8):
    if isinstance(input_image, np.ndarray):
        if encode_format == '.jpeg':
            params = [cv2.IMWRITE_JPEG_QUALITY, int(compression_level * (100 - 0) + 0)]
        elif encode_format == '.png':
            params = [cv2.IMWRITE_PNG_COMPRESSION, int(compression_level * (9 - 0) + 0)]
        else:
            return Image()
        cimage = cv2.imencode(ext=encode_format, img=input_image, params=params)
        return Image(data=cimage[1].tobytes())
    elif isinstance(input_image, Image):
        return input_image
    else:
        return Image()
    

path_images = 'src/test/images/camera' # Pasta onde as imagens serão salvas

if __name__ == '__main__':
    qnt_images = 5

    for cameraNumber in [4]:#range(1, 5): # (1, 2, 3, 4) Cameras Intelbras
        print('---RUNNING CAMERA {} CLIENT---'.format(cameraNumber))

        broker_uri = "amqp://guest:guest@10.10.2.211:30000"

        channel_1 = StreamChannel(broker_uri)

        subscription_1 = Subscription(channel=channel_1)
        subscription_1.subscribe(topic='CameraGateway.{}.Frame'.format(cameraNumber))

        window_1 = f'Intelbras Camera {cameraNumber}'

        i = 1
        time_1 = time.time()

        while i <= qnt_images:

            msg = channel_1.consume_last()  
            if type(msg) != bool: 
                im_1 = msg.unpack(Image)
                frame_1 = to_np(im_1)

            cv2.imshow(window_1, frame_1)

            #print(time.time() - time_1)

            if time.time()-time_1 > 1:
                
                time_1 = time.time()
                cv2.imwrite(f"{path_images}/image_camera{cameraNumber}_"+str(i)+".jpg", frame_1)
                i+=1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break