# Arquivos e funções para obter imagens da câmera

```
streamChannel.py
```

```py
import socket

from is_wire.core import Channel

class StreamChannel(Channel):
    def __init__(self, uri="amqp://guest:guest@localhost:5672", exchange="is"):
        super().__init__(uri=uri, exchange=exchange)

    def consume_last(self, return_dropped=False):
        dropped = 0
        try:
            msg = super().consume(timeout=0.1)
        except socket.timeout:
            return False
            
        while True:
            try:
                # will raise an exceptin when no message remained
                msg = super().consume(timeout=0.0)
                dropped += 1
            except socket.timeout:
                return (msg, dropped) if return_dropped else msg


from is_wire.core import Channel,Subscription,Message
from is_msgs.image_pb2 import Image
import time
from streamChannel import StreamChannel
```
<h2>Exemplo de uso</h2>

```py
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
    

path_images = 'path'

if __name__ == '__main__':
    print('---RUNNING CAMERA CLIENT---')


    broker_uri = "amqp://guest:guest@10.10.2.211:30000"

    channel_1 = StreamChannel(broker_uri)
 
    subscription_1 = Subscription(channel=channel_1)
    subscription_1.subscribe(topic='CameraGateway.{}.Frame'.format(3))

    window_1 = 'Intelbras Camera 1'

    i = 27
    time_1 = time.time()

    while i <= 30:
    
        msg = channel_1.consume_last()  
        if type(msg) != bool: 
            im_1 = msg.unpack(Image)
            frame_1 = to_np(im_1)
    
        cv2.imshow(window_1, frame_1)

        print(time.time() - time_1)

        if time.time()-time_1 > 1:

            time_1 = time.time()
            cv2.imwrite(f"{path_images}/image_"+str(i)+".jpg", frame_1)
            i+=1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```
