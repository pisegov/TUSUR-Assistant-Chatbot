from .Direction import Direction


class Faculty:
    def __init__(self, title, directions):
        self.title = title
        self.directions = directions

    def getDirectionByTitle(self, dirTitle):
        dirTitle = dirTitle.lower()
        for direction in self.directions:
            if direction.title.lower() == dirTitle:
                return direction
        return 0

    def getDirectionsTitles(self):
        directions_list = []
        for direction in self.directions:
            directions_list.append(direction.title)
        return directions_list
