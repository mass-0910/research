import json

with open("out_attrs.json", mode='r') as f:
    a = json.load(f)
    for k, v in a.items():
        print(v["htmlTreeBuilder0"])