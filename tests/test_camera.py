from camera_mgmt import camera_info, camera_reader, camera_capture

import unittest
import cv2
import time


class Test_Camera_Gen_Functions(unittest.TestCase):
    def test_camera_count(self):
        self.assertEqual(camera_info.get_local_available_cameras(), 1)

    def test_check_incorrect_ip_camera(self):
        self.assertEqual(camera_info.check_ip_camera("anything"), False)


class Test_CameraRead(unittest.TestCase):
    def test_create_cr(self):
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cr = camera_reader.CameraReader(video)
        self.assertIsNotNone(cr)

    def test_read_frame_cr(self):
        frame = None
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cr = camera_reader.CameraReader(video)
        cr.start()
        time.sleep(1)
        frame = cr.frame
        cr.stop()
        video.release()
        self.assertIsNotNone(frame)


class Test_CameraCapture(unittest.TestCase):
    def test_create_cc(self):
        self.assertIsNotNone(camera_capture.CameraCapture(0, 20))

    def test_cc_accessing_wrong_id_camera(self):
        with self.assertRaises(AttributeError):
            cc = camera_capture.CameraCapture(10, 20)
            cc.init()

    def test_cc_not_initialized(self):
        cc = camera_capture.CameraCapture(id=0, fps=30)
        response = cc.is_enabled()
        self.assertEqual(response, False)

    def test_cc_initialized(self):
        cc = camera_capture.CameraCapture(id=0, fps=30)
        cc.init()
        response = cc.is_enabled()
        cc.stop()
        self.assertEqual(response, True)

    def test_cc_initialized_and_released(self):
        cc = camera_capture.CameraCapture(0, 30)
        cc.init()
        cc.stop()
        self.assertEqual(cc.is_enabled(), False)

    def test_get_fps(self):
        cc = camera_capture.CameraCapture(0, 30)
        self.assertEqual(cc.fps, 30.0)

    def test_capture(self):
        cc = camera_capture.CameraCapture(0, 30)
        cc.init()
        cc.start()
        time.sleep(2)
        result = cc.is_capturing()
        cc.stop()
        self.assertEqual(result, True)

    def test_captured_frame(self):
        cc = camera_capture.CameraCapture(0, 30)
        cc.init()
        cc.start()
        time.sleep(1)
        result = cc.frame
        cc.stop()
        self.assertIsNotNone(result)

    def test_captured_bg_frame(self):
        cc = camera_capture.CameraCapture(0, 30)
        cc.init()
        cc.start()
        time.sleep(1)
        result = cc.bg_frame
        cc.stop()
        self.assertIsNotNone(result)
