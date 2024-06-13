from aiogram.types import Message
from data.requests import top_users

#Пишем словари на основе базы данных и передаем в text_top
async def top_balance(message: Message):
   dict_users = {}
   dict_balance = {}
   list_users = await top_users()
   for users in list_users:
      dict_users[users.tg_id] = users.fullname
      dict_balance[users.tg_id] = users.money_value
   print(dict_users)
   print(dict_balance)
   await text_top(message=message, dict_users=dict_users, dict_balance=dict_balance)
   
#Пишем текст:
async def text_top(message: Message, dict_users: dict, dict_balance=dict):
   text = "Топ пользователей по балансу:"
   timer = 0
   sort = sorted(dict_balance.items(), key=lambda item: item[1], reverse=True)
   user_money = sorted(dict_balance.values(), reverse=True)
   dict_id = dict(sort)
   user_id = list(dict_id.keys())
   print(f"\n\n\n{user_id}")
   print(dict_id)
   print(user_money)
   print(dict_users)
   while True:
      timer += 1
      if timer >= 11:
         break
      elif len(user_id) == 0:
         break
      else:
         username = dict_users.get(user_id.pop(0))
         text_user = f"{username}: {user_money.pop(0)}"
         text += f"\n{timer}. {text_user}"
   await message.answer(text)
   