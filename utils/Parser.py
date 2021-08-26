import requests
from bs4 import BeautifulSoup as BS
from data.model.Faculty import Faculty
from data.model.Direction import Direction


class Parser:
    def __init__(self):
        self.homepage = "https://abiturient.tusur.ru"
        r = requests.get(self.homepage + "/ru/napravleniya-podgotovki/ochnaya-forma-obucheniya")
        html = BS(r.content, "html.parser")
        self.html = html.select(".results")[0]

    def get_data(self):
        faculties = self.html.select(".educations_for")
        facultyPages = self.html.select(".educations_header_for .logotype > a")

        result_faculties = []
        index = 0

        # link = facultyLinks[0].get("href")
        while index < len(faculties):
            directionsOnFaculty = faculties[index].select("tr:not([class])")
            result_directions = []
            for direction in directionsOnFaculty:
                profiles_elements = direction.select(".profile > a")
                profiles = []
                for profile_element in profiles_elements:
                    profiles.append(profile_element.text)

                places = direction.select(".column_4 > p")

                passing_score = 0
                passing_score_element = direction.select(".column_6 > p")
                if len(passing_score_element) > 0:
                    passing_score = passing_score_element[0].text

                result_directions.append(
                    Direction(
                        title=direction.select(".column_1 > p:not([class]) > a")[0].text,
                        profiles=profiles,
                        budget_places=places[0].text,
                        passing_score=passing_score,
                        commercial_places=places[1].text,
                        price=direction.select(".column_5 > p")[0].text
                    ))

            result_faculties.append(
                Faculty(self.getFacultyTitle(facultyPages[index].get("href")), result_directions)
            )
            index += 1

        return result_faculties

    def getFacultyTitle(self, link):
        r = requests.get(self.homepage + link)
        html = BS(r.content, "html.parser")
        prefix = html.select(".breadcrumbs > *")[0].text
        title = html.select(".breadcrumbs")[0].text

        title = title.replace(prefix + " → ", '')
        # title = title.replace('факультет', '')

        return title
