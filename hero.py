#Клас hero (героя)
class Hero:
    def __init__(self, pos, land):
        self.land = land

        self.cameraOn = True
        self.spectatorMode = True

        #Загружаємо та встановлюємо координати героя, розмір
        self.hero = loader.loadModel('smiley')

        self.hero.setColor(1, 0.5, 0, 1)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        #__________________________________
        
        #Загружаємо його на карту (сцену)
        self.hero.reparentTo(render)
        #__________________

        #Прив'язка камери та включення подій
        self.cameraBind()
        self.acceptEvents()
        #________________________

    #Прив'язати камеру до гравця
    def cameraBind(self):
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)

        base.camera.setH(180)

        self.cameraOn = True
        #________________________________

    #Відв'язати камеру від гравця
    def cameraUnBind(self):
        base.enableMouse()
        base.camera.reparentTo(render)

        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 1)
        
        self.cameraOn = False
    #_________________________________

    #Сама зміна
    def ChangeCamera(self):
        if self.cameraOn:
            self.cameraUnBind()
        else:
            self.cameraBind()
    #___________________

    #Поворот наліво та направо
    def turnLeft(self):
        """
        angle = self.hero.getH()
        angle += 5
        self.hero.setH(angle)
        """
        self.hero.setH((self.hero.getH() + 5))
        
    def turnRight(self):
        self.hero.setH((self.hero.getH() - 5))
    #_________________________________________

    #Поворот преред та назад
    def turnUp(self):
        self.hero.setP((self.hero.getP() + 5))

        
    def turnDown(self):
        self.hero.setP((self.hero.getP() - 5))
    #___________________________________

    # Рухає героя на основі вказаного кута
    def just_move(self,angle):
        pos = self.lookAt(angle)
        self.hero.setPos(pos)
    #___________________________________
    def try_move(self, angle):
        pos = self.lookAt(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

        #Перевірка режиму
    def move_to(self, angle):
        if self.spectatorMode:
            self.just_move(angle)
        else:
            self.try_move(angle)
        #_________________________________

    def changeMode(self):
        #if self.spectatorMode:
            #self.spectatorMode = False
        #else:
            #self.spectatorMode = True

            self.spectatorMode = not self.spectatorMode
        
    

    #Перевірка координат

    def lookAt(self, angle):
        x = round(self.hero.getX())
        y = round(self.hero.getY())
        z = round(self.hero.getZ())

        dx, dy = self.checkDir(angle)

        return (x + dx, y + dy,z)

    def checkDir(self, angle):
        pass
        """ повертає заокруглені зміни координат X, Y,
                відповідні переміщенню у бік кута angle.
                Координата Y зменшується, якщо персонаж дивиться на кут 0,
                та збільшується, якщо дивиться на кут 180.
                Координата X збільшується, якщо персонаж дивиться на кут 90,
                та зменшується, якщо дивиться на кут 270.  
                кут 0 (від 0 до 20)      ->        Y - 1
                кут 45 (від 25 до 65)    -> X + 1, Y - 1
                кут 90 (від 70 до 110)   ->
            від 115 до 155            -> X + 1, Y + 1
                від 160 до 200            ->        Y + 1
                від 205 до 245            -> X - 1, Y + 1
                від 250 до 290            -> X - 1
                від 290 до 335            -> X - 1, Y - 1
                від 340                   ->        Y - 1  

            """
        if angle >= 0 and angle <= 20:
            return (0,-1)       
        elif angle <= 65:
            return (+1,-1)
        elif angle <= 110:
            return (+1,0)
        elif angle <= 155:
            return (+1,+1) 
        elif angle <= 200:
            return (0,+1)
        elif angle <= 245:
            return (-1,+1)
        elif angle <= 290:
            return (-1,0)
        elif angle <= 335:
            return(-1,-1)
        elif angle <= 340:
            return(0,-1)

    #_____________________________________________


        
    #Рух вперед
    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)
    #________________________________

    #Рух назад
    def backward(self):
        angle = (self.hero.getH()+ 180) % 360
        self.move_to(angle)
    #_____________________________________________

    #Рух наліво
    def left(self):
        angle = (self.hero.getH()+ 90) % 360
        self.move_to(angle)
    #__________________________________
    #Рух направо
    def right(self):
        angle = (self.hero.getH()+ 270) % 360
        self.move_to(angle)
    #__________________________________

    def up(self):
        #Якщо режим спостерігача
        if self.spectatorMode:
            #Отримати поточну z координату гравця
            pos = self.hero.getZ()
            #Додати до неї 1
            pos = pos +1  
            #Встановити нову x координату
            self.hero.setZ(pos)
        # hero = >  getZ ; setZ
        

    def down(self):
        if self.spectatorMode:
            pos = self.hero.getZ()
            pos = pos - 1
            self.hero.setZ(pos)
    

    #Підключення подій
    def acceptEvents(self):
        base.accept(change_camera_key, self.ChangeCamera)
        base.accept(change_mode_key,self.changeMode)

        base.accept(turn_left_key,self.turnLeft)
        base.accept(turn_left_key+'-repeat',self.turnLeft)

        base.accept(turn_right_key,self.turnRight)
        base.accept(turn_right_key+'-repeat',self.turnRight)

        base.accept(turn_up_key,self.turnUp)
        base.accept(turn_up_key+'-repeat',self.turnUp)

        base.accept(turn_down_key,self.turnDown)
        base.accept(turn_down_key+'-repeat',self.turnDown)


        base.accept(forward_key,self.forward)
        base.accept(forward_key + '-repeat',self.forward)

        base.accept(backward_key,self.backward)
        base.accept(backward_key + '-repeat',self.backward)

        base.accept(leftward_key,self.left)
        base.accept(leftward_key + '-repeat',self.left)

        base.accept(rightward_key,self.right)
        base.accept(rightward_key + '-repeat',self.right)

        base.accept(upward_key,self.up)
        base.accept(upward_key + '-repeat',self.up)

        base.accept(downward_key,self.down)
        base.accept(downward_key + '-repeat',self.down)


        #_____________________________________________________


#Клавіші
change_camera_key = 'c'
change_mode_key = 'z'

turn_left_key = 'arrow_left'
turn_right_key = 'arrow_right'

turn_up_key = 'arrow_up'
turn_down_key = 'arrow_down'

forward_key = 'w'
backward_key = 's'
leftward_key = 'a'
rightward_key = 'd'

upward_key = 'y'
downward_key = 'h' 

#___________________________________

