# Celeste
## Overview
This project was done for the "Tópicos de Programação para Jogos" course.  
It tries to recreate the "Celeste" game in pygame.  
Different ways of playing are offered:
- Singlelayer
- Local Multiplayer (2 players)
- Online Multiplayer (2 players)

The game has a total of 30 levels and 30 strawberries to collect.

## How to run

To run first install the requirement using the command:

```bash
pip install -r requirements.txt
```

Python version used : 3.11.0

### Singleplayer
```bash
python3 main.py
```
### Multiplayer
#### coop (shared screen)
```bash
python3 main.py -coop
```
#### online
```bash
python3 main.py -mp -p2ip <ip address of player 2>
```
The game will figure out which player is the server and which is the client automatically.

## Patterns used

### Command (Removed)
The command pattern was initially used to implement the controls of the game.  
It was used to make the controls customizable and allow 2 players to play on the same keyboard.
However, it was later removed in favor of a simpler implementation with vectors.  
See [inputhandler](inputHandler.py) for the implementation.

### Flyweight

All tiles are subsurfaces of a preloaded tileset.  
We tried to use the flyweight pattern to reduce the number of subsurfaces, however, as all tiles of the map are part of a sprite group, the tile object needed to have a `self.image` attribute.  
Assigning `self.image = flyweight.image` duplicates the image and the flyweight pattern is not used.  
The tentative implementation can be found [here](map/mapflyweight.py).

 
### Observer
Every actor is observing the player.
ex:
- The [Strawberry](actors/strawberry.py#L80) is "observing" the player to check if it is collected
- The [DashReset](actors/dashResetEntity.py#L84) is "observing" the player to check if it collected or if the player touches ground
- (...)

The notification of events from the player to the other actors is done in two places:
- [checkCorrectCollisions](actors/madeline.py#L612) - Here the player notifies all actors if it hits the [ground](actors/madeline.py#L667) or collides with a [fallingBlock](actors/madeline.py#L652) (falling clock's notification events are done here because it stops the player movement)
- [actorCollision](actors/madeline.py#L789) - Here the player notifies all actors if it collides with another actor.

The possible events that can be notified are in [Events](constants/enums.py#L49)


### Prototype
We didn't find a suitable use for the prototype pattern as it is not common the need to create new entities.

### Singleton
<!-- The serviceLocator, soundManager, inputHandler and Particle Manager classes are singletons. -->
The [serviceLocator](serviceLocator.py), [soundManager](utils/soundManager.py), [inputHandler](inputHandler.py) and [particleManager](actors/particles.py) classes are singletons.

### States / State Machine
All actors have states [Actor States](constants/enums.py#L61)
- Most of the actors can have different states. Ex: [dashReset](actors/dashResetEntity.py#L26) [fallingBlock](actors/fallingBlock.py#L24)
- Some actors only have one state. Ex: [cloud](actors/cloud.py#L23)   

The player has different states from the other actors [Player States](constants/enums.py#L20)
- The player has, in it, a state machine that regulates its state given the new inputs and current state [Player States](Actors/madeline.py#L269)

### Game Loop
The Game loop is the following:
- Process Inputs
- Load new level if needed
- Update and draw snow and clouds
- Draw Map
- Update Camera
- Update and draw actor sprites
- (multiplayer only) Draw other player
- Render 

### Update
Every actor and sprite has an update method that simulates one frame of the their behavior.

### Bytecode
The map is created using bytecode, it is read on [map.py](map/map.py#L171)
All the bytecode is on the file [maps.json](map/maps.json)   

### Subclass Sandbox
Every actor class has an update and notify sandbox method. [actor.py](actors/actor.py)

### Type object
NAo sei

### Component
The [Particle Manager](actors/particles.py) could be considered as a composite of particles as it has a list of particles which are updated and drawn. Each type of particle can be added with `addParticle()`.

### Event queue
When our client receives the position of the other player, it is added to the pygame event queue that is processed every frame. [server](server.py#L20) and [client](client.py#L19)

### Service Locator
The [serviceLocator](serviceLocator.py) is a Singleton that is used to store almost all the services of the game and make them available to all the classes that need them without having to pass them as parameters.

### Physics engine
The player has its own physics engine that determines its next position having into consideration the previous ones. [physics.py](utils/physics.py)

### Collisions
Collisions are detected using the pygame method `colliderect()` [madeline.py](actors/madeline.py#L562).
Collisions are done by simulation, the player is moved to the next position, first in the y axis and then in the x axis. If it collides with something, it is moved back to the previous position and the movement is stopped. [madeline.py](actors/madeline.py#L562)

### Events
We use events using the pygame.events.get() method to:
- Exit the game
- Draw the other player in the case of online multiplayer
- Make some keys be pressed only once every key press (jump,dash,skip_level).

### Network
The network is implemented using the websockets module with asyncio.
The game will figure out which player is the server and which is the client automatically, but this can be changed using the `-server` and `-client` flags.  
The way it works is:
- The client finishes calculating the next position of the player so it puts it in a deque that is shared with the websocket loop in a different thread.
- The websocket loop sends the position to the server.
- The server answers with the position it                            