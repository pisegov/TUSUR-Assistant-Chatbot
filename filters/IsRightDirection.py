from aiogram.dispatcher.filters import BoundFilter


class IsRightDirection(BoundFilter):
    key = "is_right_direction"

    def __init__(self, dispatcher, is_right_direction):
        self.dispatcher = dispatcher
        self.is_right_direction = is_right_direction

    async def check(self, message) -> bool:

        state = self.dispatcher.current_state(chat=message.chat.id, user=message.from_user.id)
        data = await state.get_data()
        faculty = data.get("selectedFaculty")
        direction = faculty.getDirectionByTitle(message.text)
        if not direction == 0:
            await state.update_data(selectedDirection=direction)
            return True
        return False
