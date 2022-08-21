from random import sample
from discord.ext import tasks
from calendar import c
import discord
import requests
import socket
import struct
import json
import time
import asyncio


to_connect = ()
token = ""
group_id = 123

delay = 1
delay_for_check = 2

text_for_status = " На сервере сейчас {online}/{max} игроков, заходи!"

intents = discord.Intents.default()
intents.members = True

with open("config.json", 'r', encoding='utf-8') as cfg:
    json_data=json.load(cfg)
    # print(json_data)
    token = json_data['token']
    to_connect = (json_data['ip'],json_data['port'])
    delay = json_data['delay']
    delay_for_check = json_data['delay_for_check']
    # print(to_connect)



def read_var_int(socket):
    i, j = 0, 0
    while True:
        k = socket.recv(1)
        if not k:
            return 0
        i |= (k[0] & 0x7f) << (j * 7)
        j += 1
        if not (k[0] & 0x80):
            return i

def get_online_players(ip, port):
    sock = socket.socket()
   
    sock.connect((ip, port))
    host = ip.encode('utf-8')
    data = b'\x00\x04'
    data += (struct.pack('>b', len(host)) + host + struct.pack('>H', port) ) + b'\x01'
    sock.sendall(struct.pack('>b', len(data)) + data + b'\x01\x00')
    length = read_var_int(sock)
    sock.recv(1)
    length = read_var_int(sock)
    data = bytes()

    while len(data) != length:
        data += sock.recv(length - len(data))
    sock.close()

    # with open("result.json", "w", encoding='utf-8') as json_data:
    #     json.dump(json.loads(data), json_data, indent=4)
    
    data = json.loads(data)
    if int(data["players"]["online"]) == 0:
        return "На сервере никто не чилит 😢"
    return f"На сервере чилит: {' '.join([player['name'] for player in data['players']['sample']])}"
    # return json.loads(data)
# print(get_online_players(to_connect[0],to_connect[1]))


# def update_status():
#     old_online_players = 0
#     while True:
#         online_players = get_online_players(*to_connect)
#         if old_online_players != online_players['players']['online']:
#             text = text_for_status.format(
#                 online=online_players['players']['online'],
#                 max=online_players['players']['max']
#             )
#             params = {'text': text, 'access_token': token, 'group_id': group_id, 'v': '5.122'}
#             # response = requests.post('[preview]https://api.vk.com/method/status.set', [/preview]data=params)
#             response = params
#             # print(response, "----------------------------")
#             time.sleep(delay)
#         else:
#             return(online_players['players']['online'])
#             time.sleep(delay_for_check)
           
#         old_online_players = online_players['players']['online']
# status =str(update_status())

# def get_status():
    #проверить статус
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,intents=intents, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

        # start the task to run in the background
       

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        self.my_background_task.start()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!mc'):
           await message.reply(status[1])

    @tasks.loop(seconds=1) # task runs every 60 seconds
    async def my_background_task(self):
        
        await client.change_presence(
            status= discord.Status.online, 
            activity = discord.Game(
                get_online_players(to_connect[0],to_connect[1])
            )
        )
        # channel = self.get_channel(1234567) # channel ID goes here
        # self.counter += 1
        # await channel.send(self.counter)


    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

    
if __name__ == "__main__":
    print(text_for_status)
    client = MyClient()
    client.run(token)

