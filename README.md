# pygame-multiplayer

pygame-multiplayer is an online multiplayer framework built on top of PyGame.
The goal is to abstract networking concepts for the developer in order to simplify creation of online multiplayer games.

# Example

The included file `airhockey.py` is an example game built with pygame-multiplayer.
The GameManager class is a GameObject that is not drawn which stores score.
The Puck class is a DrawableObject which represents the hockey puck and handles collisions on the server.
The Player class is a player controlled DrawableObject which is moved by mouse inputs sent from client to server.

We have included this example game in hopes that it is referenced for how game logic works in pygame-multiplayer.
Clients send inputs, the server runs game logic from those inputs, then the server sends the game state back to the clients.

## Running the air hockey server

`make run-server`

## Running the air hockey client

`make run-client`

# Todo

Add overview section to `README.md`
Write use guide