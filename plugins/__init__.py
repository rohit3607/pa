#(©)Codexbotz
#@iryme





from aiohttp import web
from .route import routes

from enum import Enum
from collections import defaultdict

class ListenerTypes(Enum):
    MESSAGE = 'message'
    # Add other listener types as needed

class YourBotClass:
    def __init__(self):
        # Other initialization code...
        self.listeners = defaultdict(list)
        # or
        # self.listeners = {listener_type: [] for listener_type in ListenerTypes}

    # Rest of your class methods...
async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app
    
