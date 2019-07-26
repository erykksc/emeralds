import renderer_pygame
import game_Module


resolution=(1280, 720)
renderer=renderer_pygame.Renderer(resolution=resolution, fullscreen=False)


renderer.updatePlayersJoined([str(i) for i in range(8)])

deck = game_Module.Deck()
tilePathNames = [deck.pickCard().getName() for _ in range(8)]
renderer.updateTileMap(tilePathNames)

renderer.showRevealedTile(tilePathNames[-1])