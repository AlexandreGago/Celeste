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
However, it was later removed in favor of a simpler implementation with vectors.  
See [inputhandler](inputHandler.py) for the implementation.

### Flyweight
- impolementar nas nuvens 
- implementar nos sptiers
- dar preload a todos os sprites
 
### Observer
Every actor is observing the player.
ex:
- The [Strawberry](actors/strawberry.py) is "observing" the player to check if it is collected
- The [DashReset](actors/dashResetEntity.py) is "observing" the player to check if it collected or if the player touches ground
- (...)

### Prototype
- nope

### Singleton
<!-- The serviceLocator, soundManager, inputHandler and Particle Manager classes are singletons. -->
The [serviceLocator](serviceLocator.py), [soundManager](utils/soundManager.py), [inputHandler](inputHandler.py) and [particleManager](actors/particles.py) classes are singletons.

### State 
The player itself is a state machine and each state lets the player do different things.

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
When our client receives the position of the other player, it is added to a queue of events that is processed every frame. [server](server.py#L21) and [client](client.py#L19)

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
(...)