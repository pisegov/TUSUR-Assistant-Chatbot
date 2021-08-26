from data.model.Direction import Direction
from utils.Parser import Parser

parser = Parser()

facultiesList = parser.get_data()

facultiesTitles = []
directionsList = []
directionsTitles = []
for faculty in facultiesList:
    facultiesTitles.append(faculty.title)
    for direction in faculty.directions:
        directionsList.append(direction)
        directionsTitles.append(direction.title)


def getItemByTitle(title, container):
    for item in container:
        if item.title == title:
            return item
    return 0