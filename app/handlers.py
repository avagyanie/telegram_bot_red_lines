import asyncio
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from app.scraper import fetch_driver_info

router = Router()

class Guest(StatesGroup):
    registration_certificate = State()
    car_number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Ողջույն։ Ընտրեք գործողությունը։",
        reply_markup=kb.main
    )

@router.message(F.text == "Որոնել որպես հյուր")
async def guest(message: Message, state: FSMContext):
    await state.set_state(Guest.registration_certificate)
    await message.answer("Խնդրում եմ լրացնել ավտոմեքենայի հաշվառման վկայագրի համարը")

@router.message(Guest.registration_certificate)
async def input_registration_certificate(message: Message, state: FSMContext):
    await state.update_data(registration_certificate=message.text)
    await state.set_state(Guest.car_number)
    await message.answer("Խնդրում եմ մուտքագրել ավտոմեքենայի պետհամարանիշը։")

@router.message(Guest.car_number)
async def input_car_number(message: Message, state: FSMContext):
    await state.update_data(car_number=message.text)
    data = await state.get_data()

    await message.answer("Տվյալները ընդունված են։ Փորձում ենք ստանալ տեղեկատվություն...")

    try:
        result = await asyncio.to_thread(
            fetch_driver_info,
            data['registration_certificate'],
            data['car_number']
        )
        await message.answer(result)
    except Exception as e:
        await message.answer("Սխալ տեղի ունեցավ։ Խնդրում ենք փորձել ավելի ուշ։")
        print(f"[ERROR] {e}")

    await state.clear()
