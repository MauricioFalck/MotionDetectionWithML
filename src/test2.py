import time

from camera_mgmt import camera_capture
from output_mgmt import display_video, video_recorder
from object_detection import object_detection
from rule_engine import rule_engine
from core import config


rule = {"detection_objects": ["person"], "schedule": {"hour": 17, "minute": 29}}

# INITIALIZATION
config_data = config.parse_config_json()
print(config_data["display_video"])
cc = camera_capture.CameraCapture(id=config_data["camera_id"], fps=config_data["fps"])
output = display_video.VideoShow()
recorder = video_recorder.VideoRecorder()
obj_detector = object_detection.ObjectDetection()
rule_eng = rule_engine.RuleEngine(rules=rule)
cc.init()
cc.start()
recorder.start()
if config_data["display_video"] == True:
    output.start()
# DETECTION
start_time = time.time()
while (time.time() - start_time) < 10:
    recorder.frame = cc.frame
    output.frame = cc.frame

# CLOSURE
obj_detector.stop()
recorder.stop()
output.stop()
cc.stop()
