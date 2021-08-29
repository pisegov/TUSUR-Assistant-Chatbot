from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from loader import dp
from data import facultiesTitles, facultiesList, getItemByTitle, directionsTitles, directionsList
from keyboards.KeyboardCreator import KeyboardCreator
from states.SelectionStates import SelectionStates
from utils import PostAdapter
from filters import IsRightDirection

dp.filters_factory.bind(IsRightDirection)


@dp.message_handler(Command("select"), state=None)
async def show_menu(message: Message):
    facultiesKeyboard = KeyboardCreator.createKeyboard(facultiesTitles, 1)
    await message.answer("Выберете факультет",
                         reply_markup=facultiesKeyboard)
    await SelectionStates.Q1_direction.set()


@dp.message_handler(Text(equals=facultiesTitles, ignore_case=True), state=SelectionStates.Q1_direction)
async def getFacultyChoice(message: Message, state=FSMContext):

    currentFacultyDirectionsTitles = []
    faculty = getItemByTitle(message.text, facultiesList)
    if faculty != 0:
        currentFacultyDirectionsTitles = faculty.getDirectionsTitles()

    keyboard = KeyboardCreator.createKeyboard(currentFacultyDirectionsTitles, 1)
    await message.answer(f"Выберете направление", reply_markup=keyboard)

    await state.update_data(selectedFaculty=faculty)

    await SelectionStates.Q2_output.set()


@dp.message_handler(Text(equals=directionsTitles), state=SelectionStates.Q2_output)
async def getDirectionChoice(message: Message, state=FSMContext):
    data = await state.get_data()
    faculty = data.get("selectedFaculty")
    direction = faculty.getDirectionByTitle(message.text)
    if direction == 0:
        direction = getItemByTitle(message.text, directionsList)

    if faculty.getDirectionsTitles().count(message.text) < 1:
        await message.answer("Это направление с другого факультета, но я все равно вам его покажу :)",
                             reply_markup=ReplyKeyboardRemove())

    outputString = f"{message.text}:\n"
    for profile in direction.profiles:
        outputString += f"-{profile}\n"
    outputString += f"Количество бюджетных мест: {direction.budget_places}\n"
    if direction.passing_score != 0:
        outputString += f"Проходной балл: {direction.passing_score}"

    await message.answer(outputString, reply_markup=ReplyKeyboardRemove())

    await state.finish()
