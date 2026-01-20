from enum import Enum


class ConnectionsStatusEnum(Enum):
    IN_MOTION_BEFORE_CLICK = 1
    IN_MOTION_AFTER_CLICK = 2
    NOT_IN_MOTION = 3
