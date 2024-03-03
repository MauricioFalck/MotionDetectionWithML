from background_subtractor.background_subtractor import BGS
import cv2
import unittest


class Test_BGS(unittest.TestCase):
    def test_BGS(self):
        bgs = BGS()
        self.assertIsNotNone(bgs)

    def test_BGS_bgsubtracted_image_is_not_none(self):
        bgs = BGS()
        img = cv2.imread("./tests/images/test.jpg")
        bgs.process_background(img)
        self.assertIsNotNone(bgs.bg_image)

    def test_BGS_detected_objects_is_not_none(self):
        bgs = BGS()
        img = cv2.imread("./tests/images/test.jpg")
        bgs.process_background(img)
        self.assertEqual(bgs.object_detected, False)
