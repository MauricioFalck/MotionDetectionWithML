import cv2


def get_local_available_cameras() -> int:
    """
    Returns the number of cameras locally connected

    Returns:
        int: the total number of cameras detected
    """
    cam_number = 0
    total_cams = 0

    while True:
        cap = cv2.VideoCapture(cam_number, cv2.CAP_DSHOW)
        cam_number += 1

        if cap.isOpened():
            total_cams += 1
            cap.release()
        else:
            return total_cams


def check_ip_camera(ip_address: str) -> bool:
    """
    Checks if a given IP camera can be accessed

    Args:
        ip_address (str): the URI of the camera

    Returns:
        bool: the response if the camera is accessible
    """
    try:
        cap = cv2.VideoCapture(ip_address)
        if cap.isOpened():
            return True
        else:
            return False
    except Exception:
        return False


def get_camera_fps(id: int | str) -> int:
    video = cv2.VideoCapture(id)
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps
