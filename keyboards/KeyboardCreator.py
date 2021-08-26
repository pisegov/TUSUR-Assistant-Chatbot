from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class KeyboardCreator:

    @staticmethod
    def createKeyboard(data_list, column_number=2):

        column_number -= 1
        if column_number < 0:
            column_number = 0
            
        keyboardMatrix = [[]]

        column_counter = 0
        row_counter = 0
        for item in data_list:
            if column_counter > column_number:
                keyboardMatrix.append([])
                row_counter += 1
                column_counter = 0
            keyboardMatrix[row_counter].append(KeyboardButton(text=item))
            column_counter += 1

        return ReplyKeyboardMarkup(
            keyboard=keyboardMatrix,
            resize_keyboard=True,
            one_time_keyboard=True
        )


