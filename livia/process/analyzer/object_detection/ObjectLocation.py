from typing import Tuple, Callable


class ObjectLocation:
    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        self.__x0 = min(x0, x1)
        self.__y0 = min(y0, y1)
        self.__x1 = max(x0, x1)
        self.__y1 = max(y0, y1)

    @property
    def x0(self) -> float:
        return self.__x0

    @property
    def y0(self) -> float:
        return self.__y0

    @property
    def x1(self) -> float:
        return self.__x1

    @property
    def y1(self) -> float:
        return self.__y1

    @property
    def coord0(self) -> Tuple[float, float]:
        return self.x0, self.y0

    @property
    def coord1(self) -> Tuple[float, float]:
        return self.x1, self.y1

    @property
    def coords(self) -> Tuple[float, float, float, float]:
        return self.x0, self.y0, self.x1, self.y1

    @property
    def height(self) -> float:
        return self.__y1 - self.__y0

    @property
    def width(self) -> float:
        return self.__x1 - self.__x0

    @property
    def area(self) -> float:
        return self.width * self.height

    def adjust_coord0(self,
                      x_adjustment: Callable[[float], float] = lambda x: x,
                      y_adjustment: Callable[[float], float] = lambda y: y,
                      reverse: bool = False) -> Tuple[int, int]:
        x = int(x_adjustment(self.__x0))
        y = int(y_adjustment(self.__y0))
        return (y, x) if reverse else (x, y)

    def adjust_coord1(self,
                      x_adjustment: Callable[[float], float] = lambda x: x,
                      y_adjustment: Callable[[float], float] = lambda y: y,
                      reverse: bool = False) -> Tuple[int, int]:
        x = int(x_adjustment(self.__x1))
        y = int(y_adjustment(self.__y1))
        return (y, x) if reverse else (x, y)

    def adjust_coords(self,
                      x_adjustment: Callable[[float], float] = lambda x: x,
                      y_adjustment: Callable[[float], float] = lambda y: y,
                      reverse: bool = False) -> Tuple[int, int, int, int]:
        x0 = int(x_adjustment(self.__x0))
        y0 = int(y_adjustment(self.__y0))
        x1 = int(x_adjustment(self.__x1))
        y1 = int(y_adjustment(self.__y1))
        return (y0, x0, y1, x1) if reverse else (x0, y0, x1, y1)

    def adjusted(self,
                 x_adjustment: Callable[[float], float] = lambda x: x,
                 y_adjustment: Callable[[float], float] = lambda y: y,
                 reverse: bool = False) -> "ObjectLocation":
        return ObjectLocation(*self.adjust_coords(x_adjustment, y_adjustment, reverse))

    def calculate_iou(self, location: "ObjectLocation") -> float:
        x0 = max(self.x0, location.x0)
        y0 = max(self.y0, location.y0)
        x1 = min(self.x1, location.x1)
        y1 = min(self.y1, location.y1)

        if x0 >= x1 or y0 >= y1:
            return 0.0
        else:
            intersection = (x1 - x0) * (y1 - y0)
            union = self.area + location.area - intersection

            return intersection / union

    def create_intersection(self, location: "ObjectLocation") -> "ObjectLocation":
        return ObjectLocation(max(self.x0, location.x0),
                              max(self.y0, location.y0),
                              min(self.x1, location.x1),
                              min(self.y1, location.y1))

    def create_union_rectangle(self, location: "ObjectLocation") -> "ObjectLocation":
        return ObjectLocation(min(self.x0, location.x0),
                              min(self.y0, location.y0),
                              max(self.x1, location.x1),
                              max(self.y1, location.y1))

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return ObjectLocation(self.__x0, self.__y0, self.__x1, self.__y1)
