from core import motion_detection
import time
import datetime

# Test case 1 - Scheduled recording
curr_time = datetime.datetime.now()
rule_1 = {"schedule": {"hour": curr_time.hour, "minute": curr_time.minute + 1}}
# Test case 2 - Motion detection
rule_2 = {"detection_objects": ["ANY"]}
# Test case 3 - Motion detection if object is a person
rule_3 = {"detection_objects": ["dog"]}
# Test case 4 - Motion detection if multiple objects are detected
rule_4 = {"detection_objects": ["person", "person", "dog"]}

x = motion_detection.MotionDetection(rules=rule_1)
print("Initiating Testcase")
x.start()
time.sleep(60)
x.stop()
print("Finalized Testcase")
