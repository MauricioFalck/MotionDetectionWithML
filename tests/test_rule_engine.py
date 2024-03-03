import cv2
import unittest
import datetime

from object_detection import yolo
from rule_engine import rule_engine


class Test_Rule_Engine(unittest.TestCase):
    def test_create_object(self):
        rule = {"detection_objects": ["person"], "schedule": "18:00"}
        self.assertIsNotNone(rule_engine.RuleEngine(rule))

    def test_create_invalid_object(self):
        rule = {"a": ["person"]}
        with self.assertRaises(AttributeError):
            rule_engine.RuleEngine(rule)

    def test_rule_not_triggered(self):
        rule = {"schedule": {"hour": 20, "minute": 00, "recurrence": False}}
        rule_eng = rule_engine.RuleEngine(rule)
        rule_eng.apply_rules()
        self.assertEqual(rule_eng.rule_triggered, False)

    def test_rule_triggered_by_schedule(self):
        curr_time = datetime.datetime.now()
        rule = {"schedule": {"hour": curr_time.hour, "minute": curr_time.minute}}
        rule_eng = rule_engine.RuleEngine(rule)
        rule_eng.apply_rules()
        self.assertEqual(rule_eng.rule_triggered, True)

    def test_rule_triggered_by_detected_obj(self):
        yolo_obj = yolo.Yolo()
        img = cv2.imread("./test.jpg")
        detected_objs = yolo_obj.process_frame(img)
        rule = {"detection_objects": ["dog"]}
        rule_eng = rule_engine.RuleEngine(rule)
        rule_eng.detected_objects = detected_objs
        rule_eng.apply_rules()
        self.assertEqual(rule_eng.rule_triggered, True)

    def test_rule_triggered_by_multiple_obj(self):
        yolo_obj = yolo.Yolo()
        img = cv2.imread("./test.jpg")
        detected_objs = yolo_obj.process_frame(img)
        rule = {"detection_objects": ["dog", "chair"]}
        rule_eng = rule_engine.RuleEngine(rule)
        rule_eng.detected_objects = detected_objs
        rule_eng.apply_rules()
        self.assertEqual(rule_eng.rule_triggered, True)

    def test_reset_trigger(self):
        yolo_obj = yolo.Yolo()
        img = cv2.imread("./test.jpg")
        detected_objs = yolo_obj.process_frame(img)
        rule = {"detection_objects": ["dog"]}
        rule_eng = rule_engine.RuleEngine(rule)
        rule_eng.detected_objects = detected_objs
        rule_eng.apply_rules()
        rule_eng.reset_trigger()
        self.assertEqual(rule_eng.rule_triggered, False)
