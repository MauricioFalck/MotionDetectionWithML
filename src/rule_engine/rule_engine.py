import datetime


class RuleEngine:
    def __init__(self, rules: dict) -> None:
        """
        Parses the rules dictionary

        Args:
            rules (dict): The rules that will be applied to the task

        Raises:
            AttributeError: Raised if a rule does not contain a scheduled task or an object detection
        """
        if "detection_objects" in rules:
            self.rule_objects_to_check = rules["detection_objects"]
        else:
            self.rule_objects_to_check = []
        if "schedule" in rules:
            self.schedule = rules["schedule"]
        else:
            self.schedule = None
        if self.rule_objects_to_check == [] and self.schedule is None:
            raise AttributeError("Invalid rule")
        if "join_rules" in rules:
            self._join_rules = rules["join_rules"]
        else:
            self._join_rules = False
        if "grace_period" in rules:
            self._grace_period = rules["grace_period"]
        else:
            self._grace_period = 0
        self.rule_triggered = False
        self.detected_objects = []

    def _check_scheduled_task(
        self,
    ) -> bool:
        """
        Checks if the schedule rule should be triggered or not

        Returns:
            bool: true if the rule is triggered
        """
        # check scheduled time rule
        if self.schedule is not None:
            target_hour = self.schedule["hour"]
            target_minute = self.schedule["minute"]
            current_time = datetime.datetime.now()
            if (
                target_hour >= current_time.hour
                and target_hour <= current_time.hour + self._grace_period
            ) and (
                target_minute >= current_time.minute
                and target_minute <= current_time.minute + self._grace_period
            ):
                return True
        return False

    def _check_object_detection(self) -> bool:
        """
        Checks if the object detection rule should be triggered or not

        Returns:
            bool: true if the rule is triggered
        """
        if self.rule_objects_to_check != []:
            for rule_obj in self.rule_objects_to_check:
                status = False
                for obj in self.detected_objects:
                    if obj["label"] == rule_obj:
                        status = True
                if status == False:
                    return False
            return True
        return False

    def apply_rules(self) -> None:
        """
        Checks if any of the rules raises the trigger.
        """
        if self._join_rules:
            if self._check_scheduled_task() and self._check_object_detection():
                self.rule_triggered = True
        else:
            if self._check_scheduled_task() or self._check_object_detection():
                self.rule_triggered = True

    def reset_trigger(self) -> None:
        """
        Resets the trigger status
        """
        self.rule_triggered = False
