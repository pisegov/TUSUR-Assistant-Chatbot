from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectionStates(StatesGroup):
    # Q0_faculty = default state
    Q1_direction = State()
    Q2_output = State()
