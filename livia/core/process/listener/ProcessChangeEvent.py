
class ProcessChangeEvent:
    def __init__(self, processor, num_frame: int):
        self.__processor = processor
        self.__num_frame = num_frame

    def processor(self):
        return self.__processor

    def num_frame(self) -> int:
        return self.__num_frame
