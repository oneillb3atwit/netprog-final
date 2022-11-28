# pygame-mp

pygame-mp is an online multiplayer framework built on top of PyGame.
By abstracting networking concepts for the developer, it makes
multiplayer game development easier for those new to programming.

# Example

The included file `airhockey.py` is an example game built with
pygame-mp. It utilizes most of the features of the engine.

We have included this example game in hopes that it is referenced for
how game logic works in pygame-mp. Clients send inputs, the server
runs game logic from those inputs, then the server sends the game
state back to the clients.

Here is a brief overview of its components:

* The GameManager class is a GameObject that is not drawn which stores
  score.
* The Puck class is a DrawableObject which represents the hockey puck
  and handles collisions on the server.  
* The Player class is a player controlled DrawableObject which is
  moved by mouse inputs sent from client to server.


## Running the air hockey server

`make run-server`

## Running the air hockey client

`make run-client`
