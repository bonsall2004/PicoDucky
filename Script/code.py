import supervisor
import time
import digitalio
from board import *
import board
from duckyinpython import *
import json
if(board.board_id == 'raspberry_pi_pico_w'):
    import wifi
    from webapp import *

config = json.load(open('./config.json'))['config']

if getAutoRun() == False:
    if((getProgrammingStatus() == False) and (config['autorun'] == True)):
      runScript(config['defaultFile'])
    else:
        print("Update your payload")

async def main_loop():
    if(board.board_id == 'raspberry_pi_pico_w'):
        webservice_task = asyncio.create_task(startWebService())
        await asyncio.gather(webservice_task)

try:
    asyncio.run(main_loop())
except (ValueError, RuntimeError) as e:
    supervisor.reload()