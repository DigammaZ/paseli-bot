import json


def get_amounts():
  with open('amounts.json') as f:
    return json.load(f)


def save(amounts):
  with open('amounts.json', 'w+') as f:
    json.dump(amounts, f)
