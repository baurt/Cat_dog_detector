
import torch
import torch.nn as nn
from torchvision import transforms as T
import os
from PIL import Image
from torchvision.models import googlenet, GoogLeNet_Weights
from PIL import Image
from PIL import Image
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message             # ловим все обновления этого типа 
from aiogram.filters.command import Command 

trnsfrms2 = T.Compose([
    T.Resize((299, 299)),
    T.ToTensor()
    ]
)

import torchvision

from torchvision.models import googlenet, GoogLeNet_Weights

model = googlenet(GoogLeNet_Weights)
model.fc=nn.Linear(1024,1)
#model with the weights trained to detect dog or cat
model.load_state_dict(torch.load('weights.pt', map_location=torch.device('cpu')))


dp = Dispatcher() 
TOKEN = os.getenv('TOKEN')
#TOKEN="6897174789:AAH8EDJrQbgapAkdggamraRF8rGaCWAcbas"
bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")



@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):    
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}!'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)
    
# 4. Обработка/Хэндлер на любые сообщения
    
@dp.message()
async def send_echo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    if message.photo:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        image_path = await bot.download_file(file_path)
        image = Image.open(image_path)
        input_tensor = trnsfrms2(image)
        input_batch = input_tensor.unsqueeze(0)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_batch = input_batch.to(device)
        model.eval()
        with torch.no_grad():              
              output = model(input_batch)  
        predicted_class_index = round(output.squeeze(-1).sigmoid().item())
        if predicted_class_index==0:
              
              await bot.send_message(chat_id=user_id, text=f"It is a cat")
        else:
              await bot.send_message(chat_id=user_id, text=f"It is a dog")

       
    else:
        await message.answer(text="Please send an image.")


# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)






