from csctracker_queue_scheduler.models.base_dto import BaseDTO


class GenericDataDTO(BaseDTO):
    msg: str

    def __init__(self, msg: str = None):
        self.msg = msg
