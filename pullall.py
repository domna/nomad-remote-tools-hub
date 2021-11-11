import json
import os

with open('tools.json', 'rt') as f:
    tools_json = json.load(f)

for tool in tools_json.values():
    image = tool.get('image')
    if not image:
        continue
    cmd = f'docker pull {image}'
    print(cmd)
    os.system(cmd)
