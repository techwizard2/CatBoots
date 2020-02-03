import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI
            initialize your snake state here using the
            request's data if necessary.
    """

    #print(json.dumps(data))

    color = '#123456'
    headType = 'fang'

    return start_response(color, headType)


@bottle.post('/move')
def move():
    data = bottle.request.json
    board = data['board']
    you = data['you']
    head = you['body'][0]

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    up = {'name': 'up', 'x': head['x'], 'y': head['y'] - 1}
    down = {'name': 'down', 'x': head['x'], 'y': head['y'] + 1}
    left = {'name': 'left', 'x': head['x'] - 1, 'y': head['y']}
    right = {'name': 'right', 'x': head['x'] + 1, 'y': head['y']}

    directions = [up, down, left, right]
    choices = {'up': 1, 'down': 1, 'left': 1, 'right': 1}

    print(json.dumps(directions[0]['x']))

    for x in you['body']:
        for y in directions:
            if y['x'] == x['x'] and y['y'] == x['y']:
                choices[y['name']] = 0

    directions.clear()

    for key, value in choices.items():
        if value == 1:
            directions.append(key)

    """
    if head['x'] == 0 and head['y'] == board['height'] - 1:
        directions = ['up', 'right']
        direction = random.choice(directions)
    elif head['x'] == board['width'] - 1 and head['y'] == board['height'] - 1:
        directions = ['up', 'left']
        direction = random.choice(directions)
    elif head['x'] == 0 or head['x'] == board['width'] - 1:
        directions = ['up', 'down']
        direction = random.choice(directions)
    else:
        directions = ['right', 'left']
        direction = random.choice(directions)
    """

    direction = random.choice(directions)
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
