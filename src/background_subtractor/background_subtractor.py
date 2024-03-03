import cv2
from core import config


class BGS:
    """
    Class that manages background subtraction activities
    """

    def __init__(self):
        """
        Initializes the BG class with a background subtracion type

        Args:
            bg_subtractor_type (str): the subtractor type to be used

        Raises:
            AttributeError: if substractor type is not recognized
        """
        config_data = config.parse_config_json()
        if config_data["bgs_subtractor_type"] == "mog2":
            self._background_subtractor = cv2.createBackgroundSubtractorMOG2()
        elif config_data["bgs_subtractor_type"] == "knn":
            self._background_subtractor = cv2.createBackgroundSubtractorKNN()
        else:
            raise AttributeError("Invalid background subtractor")
        self._threshold = config_data["bgs_threshold"]
        self.bg_image = None
        self.object_detected = False

    def process_background(self, frame: cv2.typing.MatLike) -> None:
        self.bg_image = self._subtract_background(frame)
        self.object_detected = self._detect_objects(self.bg_image)

    def _subtract_background(self, frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
        """
        Returns a negative image with objects that moved

        Args:
            frame (cv2.typing.MatLike): the frame to analyse

        Returns:
            cv2.typing.MatLike: the negative image
        """
        # Prepare the frame by removing color and blurring the image
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)
        # Apply the background subtraction algorithm
        foreground_mask = self._background_subtractor.apply(blurred_frame)
        # Apply a threshold to the fgMask
        _, subtracted_frame = cv2.threshold(
            foreground_mask, self._threshold, 255, cv2.THRESH_BINARY
        )
        return subtracted_frame

    def _detect_objects(self, frame: cv2.typing.MatLike) -> bool:
        """
        Detects objects in background image by defining coutours on objects.

        Args:
            frame (cv2.typing.MatLike): the background image to by analyzed

        Returns:
            bool: if object is detected, returns True
        """
        (contours, _) = cv2.findContours(
            frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for c in contours:
            # contourArea filters out any small contours
            if cv2.contourArea(c) < 1000:
                continue
            return True
        return False
