from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router

from BD.sql import session, Currency, Admin

from sqlalchemy import update
import decimal
#Импорт кнопок
from KeyBoards.KeyBoard import mains, mains_func, mains_admin


router = Router()


# Команада получить валюты
@router.message(F.text.lower() == "/get_currencies")
async def get_currencies(message: types.Message):
    currencies = session.query(Currency).all()
    if currencies:
        response = "Список валют с курсом к рублю:\n"
        for currency in currencies:
            response = f"{currency.currency_name}: {currency.rate} RUB\n"
            await message.answer(response)
    else:
        response = "В базе данных нет сохраненных валют."
        await message.answer(response)

class ConvertCurrency(StatesGroup):
    amount_con = State()
    curr_con = State()

# Команда конвертация
@router.message(F.text.lower() == "/convert")
async def convert_currency(message: Message, state: FSMContext):
    await state.set_state(ConvertCurrency.curr_con)
    await message.answer("Введите валюту для конвертации в формате '***':")

@router.message(ConvertCurrency.curr_con)
async def amount_currency(message: Message, state: FSMContext):
    await state.update_data(curr_con=message.text.upper())
    await state.set_state(ConvertCurrency.amount_con)
    await message.answer("Введите количество валюты:")

@router.message(ConvertCurrency.amount_con)
async def amount_currency_get(message: Message, state: FSMContext):
    await state.update_data(amount_con=message.text)
    data = await state.get_data()
    cur = data["curr_con"]
    await message.answer(f"Вы ввели {data['amount_con']} {cur}, начинаю конвертацию")

    currency = session.query(Currency).filter(Currency.currency_name == cur).first()
    try:
        if currency:
            amount = decimal.Decimal(data["amount_con"])
            converted_amount = amount * decimal.Decimal(currency.rate)
            await message.answer(f"{amount} {cur} = {converted_amount:.2f} RUB")
        else:
            await message.answer("Ошибка при конвертации. Такой валюты нет.")
    except ValueError:
        await message.answer("Некорректная сумма. Пожалуйста, введите числовое значение.")

    await state.clear()

# Админ панель
@router.message(F.text.lower() == "админ-панель")
async def admin_panel(message: Message):
    print(message.chat.id)
    user_id = message.from_user.id
    admin = session.query(Admin).filter(Admin.chat_id == str(user_id)).first()
    if admin:
        msg = message.text.lower()
        await message.answer("Перехожу в режим работы с администратором", reply_markup=mains_admin)
    else:
        await message.answer('Вам не разрешён доступ к инструментам администраторов😡', KeyBoards=mains)

# Управление валютой
@router.message(F.text.lower() == "/manage_currency")
async def manage(message: Message):
    await message.answer('Приступаю к работе с валютой', reply_markup=mains_func)

class Curstate(StatesGroup):
    cur_name = State()
    cur_rate = State()

@router.message(F.text.lower() == "добавить валюту")
async def manage(message: Message, state: FSMContext):
    await state.set_state(Curstate.cur_name)
    await message.answer('Введите название валюты')

@router.message(Curstate.cur_name)
async def process_currency_name(message: Message, state: FSMContext):
    currency_name = message.text.upper()

    # Проверяем, существует ли такая валюта уже в базе данных
    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name).first()
    if existing_currency:
        await message.answer('Данная валюта уже существует.')
        await state.clear()
    else:
        # Сохраняем название валюты в состоянии
        await state.update_data(currency_name=message.text)
        await state.set_state(Curstate.cur_rate)
        await message.answer('Введите курс к рублю')


@router.message(Curstate.cur_rate)
async def process_currency_rate(message: Message, state: FSMContext):
    await state.update_data(cur_rate=message.text)
    # Получаем сохраненные данные о валюте из состояния
    data = await state.get_data()
    currency_name = data['currency_name'].upper()
    exchange_rate = message.text

    # Создаем новую запись о валюте в базе данных
    new_currency = Currency(currency_name=currency_name, rate=float(exchange_rate))
    session.add(new_currency)
    session.commit()

    # Отправляем сообщение об успешном добавлении валюты
    await message.answer(f"Валюта {currency_name} успешно добавлена.")

    # Завершаем обработку команды
    await state.clear()

class CurstateDel(StatesGroup):
    cur_name_delete = State()

@router.message(F.text.lower() == "удалить валюту")
async def delete_currency(message: Message, state: FSMContext):
    await state.set_state(CurstateDel.cur_name_delete)
    await message.answer('Введите название валюты, которую вы хотите удалить')

@router.message(CurstateDel.cur_name_delete)
async def confirm_delete_currency(message: Message, state: FSMContext):
    currency_name = message.text.upper()
    # Проверяем, существует ли такая валюта в базе данных
    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name).first()
    if existing_currency:
        # Удаляем валюту из базы данных
        session.delete(existing_currency)
        session.commit()
        await message.answer(f'Валюта {currency_name} успешно удалена.')
    else:
        await message.answer('Данная валюта не найдена в базе данных.')

    # Завершаем обработку команды
    await state.clear()


class Curstate_new(StatesGroup):
    cur_nameNew = State()
    cur_rate_new = State()

@router.message(F.text.lower() == "изменить курс валюты")
async def change_currency_rate(message: Message, state: FSMContext):
    await state.set_state(Curstate_new.cur_nameNew)
    await message.answer('Введите название валюты, для которой вы хотите изменить курс')

@router.message(Curstate_new.cur_nameNew)
async def request_new_rate(message: Message, state: FSMContext):
    currency_name_new = message.text.upper()
    # Проверяем, существует ли такая валюта в базе данных
    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name_new).first()
    if existing_currency:
        # Сохраняем название валюты в состоянии и запрашиваем новый курс
        await state.update_data(cur_nameNew=currency_name_new)
        await state.set_state(Curstate_new.cur_rate_new)
        await message.answer('Введите новый курс к рублю для валюты')
    else:
        await message.answer('Данная валюта не найдена в базе данных.')


@router.message(Curstate_new.cur_rate_new)
async def update_currency_rate(message: Message, state: FSMContext):
    new_rate = message.text
    await state.update_data(cur_rate_new=new_rate)
    currency_name = (await state.get_data())['cur_nameNew']
    # Обновляем курс валюты в базе данных
    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name).first()
    if existing_currency:
        update_query = (
            update(Currency)
            .where(Currency.currency_name == currency_name)  # Фильтруем по имени валюты
            .values(rate=new_rate)  # Устанавливаем новое значение курса
        )
        session.execute(update_query)
        session.commit()
        await message.answer(f'Курс валюты {currency_name} успешно изменен на {new_rate}.')
    else:
        await message.answer('Ошибка при изменении курса валюты.')

    # Завершаем обработку команды
    await state.clear()


@router.message()
async def admin_panel(message: Message):
    msg = message.text.lower()
    if msg == '/назад в админ панель':
        await message.answer("Возврат к админ-панели",reply_markup=mains_admin)
    else:
        await message.answer('Возврат в общую панель',reply_markup=mains)