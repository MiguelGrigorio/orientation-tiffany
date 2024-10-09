import numpy as np

def color(point: tuple, body: tuple, desvio: int):
    
    # RGB para BGR
    body = (body[2], body[1], body[0])
    point = (point[2], point[1], point[0])
    
    # Normaliza a cor
    c_body = max(body)
    c_point = max(point)

    peso_body = np.int32(np.multiply((body[0]/c_body, body[1]/c_body, body[2]/c_body), desvio))
    peso_point = np.int32(np.multiply((point[0]/c_point, point[1]/c_point, point[2]/c_point), desvio))

    # Intervalo de cor
    color = {
        "body": {
            "lower": np.subtract(body, peso_body),
            "upper": np.add(body, peso_body)
            },
        "point": {
            "lower": np.subtract(point, peso_point),
            "upper": np.add(point, peso_point)
        }
    }
    return color