class MapManager():
    def __init__(self):
        self.startNew()
        self.model = 'block.egg'
        self.texture = 'block.png'

        self.color = (0,1,0,1)

        self.colors = [
            (0.5,0.3,0.0,1),
            (0.2,0.2,0.3,1),
            (0.5,0.5,0.2,1),
            (0.0,0.6,0.0,1),
            (0.3,0.7,0.0,1)
        ]

        self.addBlock((0,10,0))

    def startNew(self):
        self.land = render.attachNewNode('Land')

    def getColor(self,z):
        if z >= len(self.color):
            return self.colors[len(self.colors) - 1] 

        return self.colors[z]

    def addBlock(self, position: tuple[int,int,int]):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        
        #self.block.setColor(self.color)

        color = self.getColor(position[2])
        self.block.setColor(color)

        self.block.setPos(position)
        self.block.reparentTo(self.land)

        self.block.setTag('at' , str(position))

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self,filename):
        self.clear()
        with open(filename, 'r') as file:
            y = 0
            for line in file:
                x = 0
                for num in map(int,line.split(" ")):
                    for z0 in range(num):
                        self.addBlock((x,y,z0))
                    x += 1
                y += 1

    def findBlocks(self, pos):
        return self.land.findAllMatches('=at=' + str(pos))

    def isEmpty(self, pos):
        blocks: list = self.findBlocks(pos)
        if blocks:
            return False
        return  True

    def findHighestEmpty(self, pos):
        x,y,z = pos
        z = 1
        while not self.isEmpty((x,y,z)):
            z += 1
        return (x,y,z) 