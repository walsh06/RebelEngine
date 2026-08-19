"""
This is a basic demo game to show the usage of the Rebel Engine and some of its features
"""
import sys
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from rbbase.rbgame import RBGame
from rbbase.rbworld import RBWorld
from rbbase.rbplayer import RBPlayer
from rbbase.rbbase import RB2DPosition
from rbbase.rbgameobject import RBGameObjectType
from rbbase.rbgameobjects import RBRectangle, RBCircle, RBTimer, RBUpdatingText
from rbgraphics.rbgraphicsobjects import RBGraphicRectangle
from rbai.rbbehaviour import RBDespawnAfter

# Define rendering layer constants
HUD_LAYER = 0
GAME_LAYER = 1

# Define game object types
PLAYER_TYPE = RBGameObjectType(1, "Player")
COIN_TYPE = RBGameObjectType(2, "Coin")

# Subclass a game object to add game specific handling

class Player(RBPlayer):

    def __init__(self, pos):
        # Create a graphic for the player
        graphic = RBGraphicRectangle(pos, width=20, height=20, colour="black", fill="blue")
        # Call constructor for full setup
        super(Player, self).__init__(pos, graphic=graphic, speed=100, gameObjectType=PLAYER_TYPE)
        # Initialise game logic
        self.coinsCollected = 0

    def onCollision(self, other):
        """
        Handle collisions for when the player collides with another object
        """
        # Check the id of the other object to choose specific handling
        if other.ObjectTypeId == COIN_TYPE.id:
            other.removeObject()
            self.coinsCollected += 1

    def getCoinsCollected(self):
        """
        Return variable used in RBUpdatingText
        """
        return self.coinsCollected

# Define the game
class Game(RBGame):

    def __init__(self):
        # Initialize game, graphics and controller
        super(Game, self).__init__()
        self.initGraphics(500, 500)
        self.initController()
        
        # Close the game on Q being pressed
        self._controller.registerKeyFunction("q", self.quit)

        # Create a new world and add it to the game
        self.world = RBWorld(self._graphics)
        self.addWorld(self.world)

        # Create a new player with a rectangle graphic
        # Initialise its controls and add it to the world on the game layer
        self.player = Player(RB2DPosition(250, 250))
        self.player.initTopDownControls(self._controller)
        self.world.addObject(self.player, GAME_LAYER)

        # Add a timer
        self.gameTimer = RBTimer(RB2DPosition(250, 50))
        self.world.addObject(self.gameTimer, HUD_LAYER)
        self.spawnTimer = 0

        # Add updating text object to the world
        self.world.addObject(RBUpdatingText(RB2DPosition(100, 50), "Coins: {}", self.player.getCoinsCollected), HUD_LAYER)

        # Add Solid walls as the game arena
        self.world.addObject(RBRectangle(RB2DPosition(0, 100), 500, 5, fill="grey", solid=True), GAME_LAYER)
        self.world.addObject(RBRectangle(RB2DPosition(0, 100), 5, 500, fill="grey", solid=True), GAME_LAYER)
        self.world.addObject(RBRectangle(RB2DPosition(495, 100), 5, 500, fill="grey", solid=True), GAME_LAYER)
        self.world.addObject(RBRectangle(RB2DPosition(9, 495), 500, 5, fill="grey", solid=True), GAME_LAYER)

    def onUpdate(self, dt):
        """
        Overrides onUpdate of RBGame to handle behaviour we want to run every frame
        """
        super(Game, self).onUpdate(dt)

        # Handle some game specific behaviour to spawn a new coin
        self.spawnTimer += dt
        if self.spawnTimer >= 5:
            self._spawnCoin()
            self.spawnTimer = 0

    def _spawnCoin(self):
        """
        Adds a new game object to the world
        """
        pos = RB2DPosition(random.randint(50,450), random.randint(70, 450))
        # Set some default behaviour for the game object
        despawn = RBDespawnAfter(3)
        # Add the object to the world on the game layer with the COIN_TYPE
        self.world.addObject(RBCircle(pos, radius=5, colour="black", fill="gold", behaviours=[despawn], gameObjectType=COIN_TYPE), GAME_LAYER)


if __name__ == "__main__":
    # Create and run the game
    Game().run()