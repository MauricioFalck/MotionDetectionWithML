import os
import json


def parse_config_json():
    if os.path.exists(".\\config\\configuration.json"):
        with open(".\\config\\configuration.json", "r") as config_file:
            config_data = json.load(config_file)

    else:
        config_data: dict[str, int | str | bool] = {
            "camera_id": 0,
            "fps": 30,
            "stabilization_time": 3,
            "video_duration": 10,
            "display_video": False,
            "destination_folder": ".\\outputs",
            "bgs_subtractor_type": "mog2",
            "bgs_threshold": 200,
            "obd_score_threshold": 0.5,
            "obd_nms_threshold": 0.45,
            "obd_confidence_threshold": 0.45,
            "obd_input_width": 640,
            "obd_input_height": 640,
        }
        with open(".\\config\\configuration.json", "w") as config_file:
            json.dump(config_data, config_file)
    return config_data
