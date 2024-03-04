import unittest
import cv2
from object_detection import yolo, object_detection


class Test_Yolo(unittest.TestCase):
    def test_create_yolo_object(self):
        self.assertIsNotNone(yolo.Yolo())

    def test_get_valid_yolo_response(self):
        yolo_obj = yolo.Yolo()
        img = cv2.imread("./tests/images/test.jpg")
        detected_objs = yolo_obj.process_frame(img)
        self.assertIsNotNone(len(detected_objs) > 0)


class Test_ObjectDetection(unittest.TestCase):
    def test_create_obj_detection_object(self):
        self.assertIsNotNone(object_detection.ObjectDetection())

    def test_obj_detect_not_running(self):
        obj_detect = object_detection.ObjectDetection()
        self.assertEqual(obj_detect.is_running(), False)

    def test_obj_detect_is_running(self):
        obj_detect = object_detection.ObjectDetection()
        obj_detect.start()
        result = obj_detect.is_running()
        obj_detect.stop()
        self.assertEqual(result, True)
