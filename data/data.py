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
    title = title.lower()

    for item in container:
        if item.title.lower() == title:
            return item
    return 0
