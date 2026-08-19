# RebelEngine

The Rebel Engine is a basic python game framework/engine for 2D games. The framework code is located in the src folder and can be imported into any python script. Its written with python 3. The test folder contains some basic examples that use various aspects of the framework. 

- [Demo Game](test/demos/demoGame.py)

## Current Features

- [**RBGame ready to run()**](src/rbbase/rbgame.py): Just implement your own version of RBGame and most of the underlying game loop is already handled for you.
- [**RBGameObject**](src/rbbase/rbgameobject.py): Game objects can be added to your game easily with an existing library of useful objects. Very extensible for whatever you want to add to your game.
- [**RBGraphics**](src/rbgraphics/rbgraphicsobjects.py): Plenty of graphical support in text, shapes, images and animated sprites.
- [**RBSound**](src/rbsound/rbsound.py): Play sounds in your game quickly and easily.
- [**RBCollision**](src/rbphysics/rbcollision.py): Collision detection between game objects is already supported once a RBBoundingBox or RBBoundingCirlce is in place. Handle the collision how you want after that.
- [**RBBehaviour**](src/rbai/rbbehaviour.py): Set of default behaviours that can be applied to any game object to perform some basic actions. Takes the effort away from manual handling in onUpdate of each object.
