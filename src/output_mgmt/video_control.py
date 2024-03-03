import os
import json
from core import config


class VideoControlMgmt:
    def __init__(self) -> None:
        config_data = config.parse_config_json()
        self.detection_file = os.path.join(
            config_data["destination_folder"], "detection_info.json"
        )
        self._read_detection_data()

    def get(self) -> list[dict]:
        return self._video_data

    def add(self, entry: dict) -> None:
        # validate entry
        self._video_data.append(entry)
        self._save()

    def remove(self, index) -> None:
        del self._video_data[index]
        self._save()
        self.refresh()

    def refresh(self):
        self._read_detection_data()

    def _save(self):
        if os.path.exists(self.detection_file):
            os.remove(self.detection_file)
        with open(self.detection_file, "w") as output_file:
            json.dump({"detection_videos": self._video_data}, output_file)

    def _read_detection_data(self):
        if os.path.exists(self.detection_file):
            # read json
            with open(self.detection_file, "r") as input_file:
                parsed_data = json.load(input_file)
                self._video_data = parsed_data["detection_videos"]
        else:
            self._video_data = []
