#returns a tile map surface from an 2d array Arr of string names of the tiles

if resolution=="AUTO":
    resolution = self.displaySurface.get_size()

#tileSize=math.floor(self.displayRes[0]/self.tilesPerRow) #OG version
lenX = len(tileMap[0]) #length of tiles array that are going to be displayed horizontally
lenY = len(tileMap) #length of tiles array that are going to be displayed vertically
if (lenY >= lenX) or (lenX/lenY<(resolution[0]/resolution[1])): #check if tile map has more tiles in y
    tileSize=math.floor(resolution[1]/len(tileMap))
else:
    tileSize=math.floor(resolution[0]/len(tileMap[0]))

#calculates the starting position at x and y coordinates
xGap = (resolution[0] - tileSize*len(tileMap[0]))/2
yGap = (resolution[1] - tileSize*len(tileMap))/2

tileMapSurface = pygame.Surface((resolution))

if background=="fill_black":
    tileMapSurface.fill((0,0,0))
else:
    resizedBackground = pygame.transform.scale(background, (resolution))
    tileMapSurface.blit(resizedBackground, (0,0))

xPos = xGap
yPos = yGap
tileToPlace = pygame.Surface((tileSize, tileSize))
for x in range(len(tileMap)):
    for y in range(len(tileMap[x])):
        tileTexture = self.getTileTexture(tileMap[x][y])
        tileToPlace = pygame.transform.scale(tileTexture, (tileSize, tileSize))
        tileMapSurface.blit(tileToPlace , (xPos, yPos))
        xPos += tileSize
    yPos += tileSize
    xPos = xGap

return tileMapSurface
