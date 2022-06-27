from numpy import ndarray, ascontiguousarray


class AreaOfInterest:
    def __init__(self, x: int, y: int, width: int, height: int):
        if x < 0:
            raise ValueError("x must be non-negative number")
        if y < 0:
            raise ValueError("y must be non-negative number")
        if width < 1:
            raise ValueError("width must be a positive number")
        if height < 1:
            raise ValueError("height must be a positive number")

        self.__x: int = x
        self.__y: int = y
        self.__width: int = width
        self.__height: int = height

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def x0(self) -> int:
        return self.__x

    @property
    def y0(self) -> int:
        return self.__y

    @property
    def x1(self) -> int:
        return self.__x + self.__width - 1

    @property
    def y1(self) -> int:
        return self.__y + self.__height - 1

    def extract_from(self, frame: ndarray) -> ndarray:
        frame_aoi = frame[self.y0:self.y1 + 1, self.x0:self.x1 + 1]

        return frame_aoi if frame_aoi.flags['C_CONTIGUOUS'] else ascontiguousarray(frame_aoi)

    def replace_on(self, frame: ndarray, aoi: ndarray) -> ndarray:
        for x in range(self.x0, self.x1 + 1):
            for y in range(self.y0, self.y1 + 1):
                frame[y, x] = aoi[y - self.y, x - self.x]

        return frame
