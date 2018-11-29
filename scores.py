import json

def reset():
    with open('defaultscores.json') as file:
    # with open('debugscores.json') as file:
        RESET = json.load(file)

    with open('highscores.json', 'w') as file:
        json.dump(RESET, file, indent=2)

def load():
    with open('highscores.json') as file:
        data = json.load(file)
    return data

def insertScore(score, name):
    data = load()
    data.append({'amount': score, 'name': name})
    data = sorted(data, key=lambda i: i['amount'], reverse=True)[:10]
    lastIndex = None
    if ({'amount': score, 'name': name} in data):
        lastIndex = data.index({'amount': score, 'name': name})
    with open('highscores.json', 'w') as file:
        json.dump(data, file, indent=2)
    return lastIndex
