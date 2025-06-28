from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb


router = Router()


class Guest(StatesGroup):
    registration_certificate = State()
    car_number = State()

class Register(StatesGroup):
    name = State()
    age = State()
    registration_certificate = State()
    car_number = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Ողջույն: Եթե ցանկանում եք պարբերաբար ստանալ ծանուցումներ կարմիր գծերի խախտումների վերաբերյալ, ապա գրանցվեք որպես օգտատեր կամ ընտրեք «Որոնել որպես հյուր» տարբերակը՝ պարզապես դիտելու համար:", reply_markup=kb.main)

@router.message(F.text == "Որոնել որպես հյուր")
async def guest(message: Message, state: FSMContext):
    await state.set_state(Guest.registration_certificate)
    await message.answer("Խնդրում եմ լրացնել ավտոմեքենայի հաշվառման վկայագրի համարը")

@router.message(Guest.registration_certificate)
async def registration_certificate(message: Message, state: FSMContext):
    await state.update_data(registration_certificate=message.text)
    await state.set_state(Guest.car_number)
    await message.answer("Խնդրում եմ լրացնել ավտոմեքենայի պետհամարանիշը")

@router.message(Guest.car_number)
async def car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    data = await state.get_data()
    await message.answer(f"Ձեր ավտոմեքենայի հաշվառման վկայագրի համարն է  {data['registration_certificate']}\nՁեր ավտոմեքենայի պետհամարանիշն է {data['car_number']}: Խնդրում եմ սպասել պատասխանին:")
    await state.clear()
 

@router.message(F.text == "Գրանցվել")
async def catalog(message: Message):
    await message.answer("Select what you're interested in", reply_markup=kb.catalog)
