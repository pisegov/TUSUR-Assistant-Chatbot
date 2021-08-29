from data.model import Direction


class PostAdapter:

    @staticmethod
    def makePost(direction):
        outputString = f"{direction.title}:\n"
        for profile in direction.profiles:
            outputString += f"-{profile}\n"
        outputString += f"Количество бюджетных мест: {direction.budget_places}\n"
        if direction.passing_score != 0:
            outputString += f"Проходной балл: {direction.passing_score}"

        return outputString
