import unittest
from output_mgmt import video_control, video_recorder, generic
from camera_mgmt import camera_capture
import os
import time


class TestGenericRecorder(unittest.TestCase):
    def test_prepare_number_with_leading_0(self):
        self.assertEqual(generic.prepare_number(1), "01")

    def test_prepare_number_without_leading_0(self):
        self.assertEqual(generic.prepare_number(10), "10")


class TestVideoRecorder(unittest.TestCase):
    def test_recorder_object(self):
        self.assertIsNotNone(video_recorder.VideoRecorder())

    def test_recorded_file_exists(self):
        cc = camera_capture.CameraCapture(id=0, fps=30)
        cc.init()
        cc.start()
        recorder = video_recorder.VideoRecorder()
        recorder.frame = cc.frame
        recorder.start()
        file_name = recorder.filename
        start_time = time.time()
        while (time.time() - start_time) < 2:
            recorder.frame = cc.frame
        recorder.stop()
        cc.stop()
        self.assertEqual(os.path.exists(os.path.join(".\\outputs\\", file_name)), True)


class TestVideoManagement(unittest.TestCase):
    def test_create_VideoManagement(self):
        self.assertIsNotNone(video_control.VideoControlMgmt())

    def test_get_entries(self):
        vm = video_control.VideoControlMgmt()
        self.assertEqual(len(vm.get()), 0)

    def test_add_entry(self):
        if os.path.exists(".\\outputs\\detection_info.json"):
            os.remove(".\\outputs\\detection_info.json")
        vm = video_control.VideoControlMgmt()
        entry = {"a": 1}
        vm.add(entry)
        self.assertEqual(len(vm.get()), 1)

    def test_save_output_file(self):
        if os.path.exists(".\\outputs\\detection_info.json"):
            os.remove(".\\outputs\\detection_info.json")
        vm = video_control.VideoControlMgmt()
        entry = {"a": 1}
        vm.add(entry)
        vm._save()
        self.assertEqual(os.path.exists(vm.detection_file), True)

    def test_parse_existing_data(self):
        if os.path.exists(".\\outputs\\detection_info.json"):
            os.remove(".\\outputs\\detection_info.json")
        vm = video_control.VideoControlMgmt()
        entry = {"a": 1}
        vm.add(entry)
        vm.add(entry)
        vm._save()
        vm2 = video_control.VideoControlMgmt()
        self.assertEqual(len(vm2.get()), 2)

    def test_remove_entry(self):
        if os.path.exists(".\\outputs\detection_info.json"):
            os.remove(".\\outputs\detection_info.json")
        vm = video_control.VideoControlMgmt()
        entry1 = {"a": 1}
        entry2 = {"a": 2}
        vm.add(entry1)
        vm.add(entry2)
        vm.remove(0)
        entries = vm.get()
        self.assertEqual(entries[0]["a"], 2)
