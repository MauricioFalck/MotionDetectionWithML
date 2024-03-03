from threading import Thread
import cv2
from typing import Self


class VideoShow:
    """
    Class that continuously shows on a window the captured frames using a dedicated thread.
    """

    def __init__(self):
        """
        Initializes the VideoShow object
        """
        self.frame = None
        self.bg_frame = None
        self.stopped = False

    def start(self) -> Self:
        """
        Starts to display the frames on a window
        """
        Thread(target=self._show, args=()).start()
        return self

    def _show(self):
        """
        The process that runs continuosly displayig every captured frame on a window
        """
        while not self.stopped:
            cv2.waitKey(int((1 / 30) * 1000))
            if self.frame is not None:
                cv2.imshow("Video", self.frame)
                if self.bg_frame is not None:
                    cv2.imshow("BG", self.bg_frame)
        cv2.destroyAllWindows()

    def stop(self):
        """
        Stops to display the frames
        """
        self.stopped = True
