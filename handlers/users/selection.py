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
async def showMenu(message: Message):
    keyboard = KeyboardCreator.createKeyboard(facultiesTitles, 1)
    await message.answer("Выберете факультет",
                         reply_markup=keyboard)
    await SelectionStates.Q1_direction.set()


@dp.message_handler(Text(equals=facultiesTitles, ignore_case=True), state=SelectionStates.Q1_direction)
async def getFacultyChoice(message: Message, state=FSMContext):

    faculty = getItemByTitle(message.text, facultiesList)
    keyboard = KeyboardCreator.createKeyboard(faculty.getDirectionsTitles(), 1)
    await message.answer(f"Выберете направление", reply_markup=keyboard)

    await state.update_data(selectedFaculty=faculty)

    await SelectionStates.Q2_output.set()


@dp.message_handler(state=SelectionStates.Q1_direction)
async def getWrongFacultyChoice(message: Message, state=FSMContext):
    keyboard = KeyboardCreator.createKeyboard(facultiesTitles, 1)
    await message.answer("К сожалению, я не нашел такого факультета :(\n"
                         "Попробуйте еще раз",
                         reply_markup=keyboard)


@dp.message_handler(is_right_direction=True, state=SelectionStates.Q2_output)
async def getRightDirectionChoice(message: Message, state=FSMContext):
    data = await state.get_data()
    direction = data.get("selectedDirection")

    await message.answer(PostAdapter.makePost(direction), reply_markup=ReplyKeyboardRemove())

    await state.finish()


@dp.message_handler(Text(equals=directionsTitles, ignore_case=True), state=SelectionStates.Q2_output)
async def getExistingDirectionChoice(message: Message, state=FSMContext):

    direction = getItemByTitle(message.text, directionsList)

    await message.answer("Это направление с другого факультета, но я все равно вам его покажу :)",
                         reply_markup=ReplyKeyboardRemove())

    await message.answer(PostAdapter.makePost(direction), reply_markup=ReplyKeyboardRemove())

    await state.finish()


@dp.message_handler(state=SelectionStates.Q2_output)
async def getWrongDirectionChoice(message: Message, state=FSMContext):
    data = await state.get_data()
    faculty = data.get("selectedFaculty")
    keyboard = KeyboardCreator.createKeyboard(faculty.getDirectionsTitles(), 1)

    await message.answer(f"К сожалению, я не нашел такого направления :(\n"
                         "Попробуйте еще раз", reply_markup=keyboard)
