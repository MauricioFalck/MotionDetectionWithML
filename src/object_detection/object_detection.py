from object_detection import yolo
from threading import Thread


class ObjectDetection:
    """
    Class that records every captured frame to an output file using a dedicated thread.
    """

    def __init__(self):
        self.detected_objects = []
        self.frame = None
        self._thread = None
        self._yolo = yolo.Yolo()
        self._stopped = True

    def start(self) -> None:
        self._stopped = False
        Thread(target=self._check).start()

    def stop(self) -> None:
        self._stopped = True

    def _check(self) -> None:
        while not self._stopped:
            if self.frame is not None:
                self.detected_objects = self._yolo.process_frame(self.frame)

    def is_running(self) -> bool:
        return not self._stopped
