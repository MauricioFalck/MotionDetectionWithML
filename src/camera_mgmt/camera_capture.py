import cv2
from camera_mgmt import camera_reader, camera_info
from background_subtractor import background_subtractor
from threading import Thread


class CameraCapture:
    def __init__(
        self,
        id: int | str,
        fps: int,
    ) -> None:
        """
        Init the CameraCapture class

        Args:
            id (int | str): the ID of the camera (number or URI)
            bg_subtractor (background_subtractor.BGS_Type, optional): The background subtractor type to be used. Defaults to background_subtractor.BGS_Type.MOG2.
        """
        self.camera_id = id
        self.width = 0
        self.height = 0
        self.fps = fps
        self.frame = None
        self.bg_frame = None
        self.motion_detected = False
        self._bg_sub = background_subtractor.BGS()
        self._capture_thread = None

    def init(self) -> None:
        """
        Initializes the camera provided in the initialization of the class

        Raises:
            AttributeError: if camera cannot be reached
        """
        try:
            # Initialize video capture
            self._video_capture = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
            # Set the fps
            self._video_capture.set(cv2.CAP_PROP_FPS, self.fps)
            # Init the camera reader
            self._camera_reader = camera_reader.CameraReader(self._video_capture)
            # Get height and width of capture
            self._height = self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self._width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            if self._height == 0 and self.width == 0:
                raise AttributeError("Invalid camera ID")
            # Creates the thread object
            self._capture_thread = Thread(target=self._capture)
            self._stopped = True

        except AttributeError:
            raise AttributeError("Invalid camera ID")

    def _capture(self) -> None:
        """
        Captures the stream from the camera
        """
        reader = camera_reader.CameraReader(self._video_capture)
        reader.start()
        while not self._stopped:
            self.frame = reader.frame
            self._bg_sub.process_background(self.frame)
            self.bg_frame = self._bg_sub.bg_image
            self.motion_detected = self._bg_sub.object_detected
        reader.stop()

    def start(self) -> None:
        """
        Starts capturing frames from the camera input
        """
        self._stopped = False
        self._capture_thread.start()

    def stop(self) -> None:
        """
        Stops capturing the frames from the camera input
        """
        self._stopped = True
        if self._capture_thread.is_alive():
            self._capture_thread.join()
        self._video_capture.release()

    def is_capturing(self) -> bool:
        """
        Checks if the camera is capturing frames

        Returns:
            bool: True if camera is capturing frames
        """
        return self._capture_thread.is_alive()

    def is_enabled(self) -> bool:
        """
        Checks if the camera is enabled

        Returns:
            bool: True if camera is enabled
        """
        try:
            return self._video_capture.isOpened()
        except:
            return False
