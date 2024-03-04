from threading import Thread
import cv2


class CameraReader:
    """
    Class that continuously gets frames from a VideoCapture object
    in a dedicated thread.
    """

    def __init__(self, video_capture: cv2.VideoCapture):
        """
        Initializes the CameraReader object

        Args:
            video_capture (cv2.VideoCapture): The VideoCapture object to be used - Must be initialized before using
        """
        self.stream = video_capture
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        """
        Starts to capture frames from the camera
        """
        Thread(target=self._read, args=()).start()
        self.stopped = False

    def _read(self):
        """
        Reads the frame from the camera and assigns it to the frame property. In case there is an error
        when reading, the grabbed property will be False
        """
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        """
        Stops reading the frames from the camera
        """
        self.stopped = True
