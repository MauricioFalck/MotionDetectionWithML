from typing import Any
from core import config
import cv2
import numpy as np


class Yolo:
    def __init__(self) -> None:
        """
        Initializes the Yolo object detection class

        Raises:
            AttributeError: exception raised if any of the attributes is higher than 1 or lower than 0
        """
        # Load config data
        config_data = config.parse_config_json()
        # Load classes names
        classesFile = "./models/coco.names"
        self.classes = None
        with open(classesFile, "rt") as f:
            self.classes = f.read().rstrip("\n").split("\n")
        self._net = cv2.dnn.readNet("./models/yolov5s.onnx")
        self.input_width = config_data["obd_input_width"]
        self.input_height = config_data["obd_input_height"]
        if (
            (
                config_data["obd_score_threshold"] > 1
                or config_data["obd_score_threshold"] < 0
            )
            or (
                config_data["obd_nms_threshold"] > 1
                or config_data["obd_nms_threshold"] < 0
            )
            or (
                config_data["obd_confidence_threshold"] > 1
                or config_data["obd_confidence_threshold"] < 0
            )
        ):
            raise AttributeError()
        self._score_threshold = config_data["obd_score_threshold"]
        self._nms_threshold = config_data["obd_nms_threshold"]
        self._confidence_threshold = config_data["obd_confidence_threshold"]

    def process_frame(self, frame: cv2.typing.MatLike) -> list:
        """
        Provides a list of the object detected

        Args:
            frame (np.ndarray): the frame to be analyzed

        Returns:
            list: a list that describes the objects detected
        """
        # Process image.
        detections = self._pre_process(frame)
        objects_detected = self._post_process(frame, detections)
        return objects_detected

    def _pre_process(self, image: cv2.typing.MatLike) -> Any:
        """
        Runs the image over the Yolo model

        Args:
            image (np.ndarray): the image to be analyzed

        Returns:
            : _description_
        """
        # Create a 4D blob from a frame
        blob = cv2.dnn.blobFromImage(
            image,
            1 / 255,
            (self.input_width, self.input_height),
            [0, 0, 0],
            1,
            crop=False,
        )
        # Sets the input to the network
        self._net.setInput(blob)
        # Runs the forward pass to get output of the output layers
        output_layers = self._net.getUnconnectedOutLayersNames()
        outputs = self._net.forward(output_layers)
        return outputs

    def _post_process(self, input_image: cv2.typing.MatLike, outputs: list) -> list:
        # Lists to hold respective values while unwrapping.
        class_ids = []
        confidences = []
        boxes = []

        # Rows
        rows = outputs[0].shape[1]

        image_height, image_width = input_image.shape[:2]

        # Resizing factor.
        x_factor = image_width / self.input_width
        y_factor = image_height / self.input_height

        # Iterate through 25200 detections
        for r in range(rows):
            row = outputs[0][0][r]
            confidence = row[4]

            # Discard bad detections and continue.
            if confidence >= self._confidence_threshold:
                classes_scores = row[5:]

                # Get the index of max class score.
                class_id = np.argmax(classes_scores)

                #  Continue if the class score is above threshold.
                if classes_scores[class_id] > self._score_threshold:
                    confidences.append(confidence)
                    class_ids.append(class_id)

                    cx, cy, w, h = row[0], row[1], row[2], row[3]

                    x = int((cx - w / 2) * x_factor)
                    y = int((cy - h / 2) * y_factor)
                    w = int(w * x_factor)
                    h = int(h * y_factor)

                    box = np.array([x, y, w, h])
                    boxes.append(box)

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv2.dnn.NMSBoxes(
            boxes, confidences, self._confidence_threshold, self._nms_threshold
        )
        detected_objects = []
        for i in indices:
            box = boxes[i]
            detected_objects.append(
                dict(
                    label=self.classes[class_ids[i]],
                    confidence=confidences[i],
                    x=box[0],
                    y=box[1],
                    w=box[2],
                    h=box[3],
                )
            )
        return detected_objects
