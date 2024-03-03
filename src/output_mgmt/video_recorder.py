from threading import Thread
from output_mgmt import generic, video_control
from core import config
import cv2
import os
import time


class VideoRecorder:
    """
    Class that records every captured frame to an output file using a dedicated thread.
    """

    def __init__(self) -> None:
        """
        Initializes the Recorder object
        """
        config_data = config.parse_config_json()
        if config_data["video_duration"] > 0 and config_data["fps"] > 0:
            self.duration = config_data["video_duration"]
            self.fps = config_data["fps"]
        else:
            raise AttributeError("VideoRecorder: Invalid Attributes")
        self.frame = None
        self.video_writer = None
        self._stopped = True
        self._thread = None
        self.start_time = None
        self.filename = None
        self._folder = config_data["destination_folder"]
        if not os.path.exists(self._folder):
            raise AttributeError("VideoRecorder: Invalid destination folder")

    def start(self) -> None:
        """
        Starts the recording the video to a file
        """
        if self._stopped:
            self.filename = generic.get_filename()
            self.video_writer = cv2.VideoWriter(
                os.path.join(self._folder, self.filename),
                cv2.VideoWriter.fourcc(*"mp4v"),
                self.fps,
                (640, 480),
            )
            self.start_time = time.time()
            self._stopped = False
            Thread(target=self._write).start()

    def _write(self) -> None:
        """
        The process that runs continously grabbing frames and adding to a file
        """
        if self.start_time is not None and self.video_writer is not None:
            while not self._stopped:
                time.sleep(1 / self.fps)
                if self.frame is None:
                    continue
                self.video_writer.write(self.frame)
                if (time.time() - self.start_time) >= self.duration:
                    self.stop()
            self.start_time = None

    def stop(self) -> None:
        """
        Stops collecting the frames and closes the output file
        """
        if self.is_running():
            self._stopped = True
            if self.video_writer is not None:
                # saves the mp4 to disk
                self.video_writer.release()
                video_mgmt = video_control.VideoControlMgmt()
                video_mgmt.add({"name": self.filename})
            self.filename = None

    def is_running(self) -> bool:
        """
        Returns a boolean with the state of the VideoRecorder

        Returns:
            bool: True if the writer is saving data to a file
        """
        return not self._stopped
