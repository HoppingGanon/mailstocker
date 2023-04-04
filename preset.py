
import json

def getPresets():
    o = open('presets.json', 'r', encoding='utf-8')
    s = o.read()
    d = json.loads(s)

    presets = Presets(len(d.get('servers')))
    
    for i, p in enumerate(d.get('servers')):
        presets.servers[i].name = (p.get('name'))
        presets.servers[i].rcv_server = (p.get('rcv_server'))
        presets.servers[i].rcv_port = (p.get('rcv_port'))
        presets.servers[i].rcv_method = (p.get('rcv_method'))
        presets.servers[i].memo = (p.get('memo'))
    

class PresetServer:
    def __init__(self):
        self.name = ''
        self.rcv_server = ''
        self.rcv_port = ''
        self.rcv_method = ''
        self.memo = ''

    name: str
    rcv_server: str
    rcv_port: str
    rcv_method: str
    memo: str

class Presets:
    def __init__(self, count: int):
        self.servers = [ PresetServer() ] * count

    servers: list[PresetServer]
