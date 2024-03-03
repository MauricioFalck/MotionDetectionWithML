import time
from camera_mgmt import camera_capture
from output_mgmt import display_video, video_recorder, video_control
from object_detection import object_detection
from rule_engine import rule_engine
from core import config
from threading import Thread


class MotionDetection:
    def __init__(self, rules: dict) -> None:
        """
        Initializes the motion detection
        """
        config_data = config.parse_config_json()
        self._camera_capture = camera_capture.CameraCapture(
            id=config_data["camera_id"], fps=config_data["fps"]
        )
        self._stabilization_time = config_data["stabilization_time"]
        self._video_output = display_video.VideoShow()
        self._recorder = video_recorder.VideoRecorder()
        self._obj_detector = object_detection.ObjectDetection()
        self._rule_eng = rule_engine.RuleEngine(rules=rules)
        self._stopped = True
        self._display_video = config_data["display_video"]

    def start(self) -> None:
        """
        Starts the MotionDetection process
        """
        if self._stopped:
            self._camera_capture.init()
            self._camera_capture.start()
            if self._display_video:
                self._video_output.start()
            self._stopped = False
            Thread(target=self._main_process).start()

    def _main_process(self):
        """
        Process that executes the motion detection process
        """
        start_time = time.time()
        action_executed = False
        stabilization_reached = False
        while not self._stopped:
            # copies the captured frame to the output components
            self._recorder.frame = self._camera_capture.frame
            self._video_output.frame = self._camera_capture.frame
            # Only runs the detection code if requested in the rules
            if self._rule_eng.rule_objects_to_check != []:
                # wait some time (stabilization time) for the background subtractor to adjust
                if not stabilization_reached:
                    if (time.time() - start_time) >= self._stabilization_time:
                        stabilization_reached = True
                else:
                    # only detects objects if the rule is not yet triggered
                    if not self._rule_eng.rule_triggered:
                        # checks is the background detector detected motion
                        if self._camera_capture.motion_detected:
                            # check if the rules are asking for simple motion detection
                            if self._rule_eng.rule_objects_to_check == ["ANY"]:
                                self._rule_eng.rule_triggered = True
                            else:
                                # feed the captured frame to the object detector component
                                self._obj_detector.frame = self._camera_capture.frame
                                # start the detector if it is not running
                                if not self._obj_detector.is_running():
                                    self._obj_detector.start()
                                # feed the rule engine with the detected objects
                                self._rule_eng.detected_objects = (
                                    self._obj_detector.detected_objects
                                )
                        else:
                            self._obj_detector.stop()
            # apply the rules with the current data
            # checks if the rule condition was triggered
            if self._rule_eng.rule_triggered:
                # The code below will only run once after the rule is triggered
                if not self._recorder.is_running() and not action_executed:
                    self._recorder.start()
                    action_executed = True
            else:
                self._rule_eng.apply_rules()

    def stop(self):
        self._stopped = True
        self._obj_detector.stop()
        self._recorder.stop()
        self._video_output.stop()
        self._camera_capture.stop()

    def is_running(self):
        return not self._stopped
