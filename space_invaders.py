'''
All images, sounds, icon and font are downloaded from internet under CC0 and CC1 licenses.
'''

# import libraries
import sys, pygame, math

class MyGame(object):
    '''
    Class defining the game. Behaves both as a view and a controller.
    '''

    # constructor
    def __init__(self):

        # initialize the game
        pygame.init()

        # window size defined as two variables
        self._size = self._width, self._height = 720, 560
        # load background image
        self._bg = pygame.image.load("./images/bg.png")
        # load background color
        self._black = 0, 0, 0
        
        # representation of the surface/screen
        self._screen = pygame.display.set_mode(self._size)

        # define the caption of the screen
        pygame.display.set_caption("Space Invaders")
        # load an image of an icon
        self._icon = pygame.image.load("./images/icon.svg")
        # set icon of the screen
        pygame.display.set_icon(self._icon)
        
        # load fonts to the game
        self._font = pygame.font.Font('./font/ExpressionPro.otf', 30)
        self._font_bigger = pygame.font.Font('./font/ExpressionPro.otf', 50)

        # load background music to the game
        self._bg_music = pygame.mixer.Sound("./sounds/space-invaders.wav")
        # set the volume of the background music
        self._bg_music.set_volume(0.02)

        # load sound effect to the game
        # load sound effect for shooting
        self._shoot_sound = pygame.mixer.Sound("./sounds/shoot.wav")
        # load sound effect for when the alien gets shot
        self._alien_killed_sound = pygame.mixer.Sound("./sounds/invaderkilled.wav")
        # load sound effect for when the player gets killed
        self._player_killed_sound = pygame.mixer.Sound("./sounds/explosion.wav")

        # load the image of the ship
        self._shipview = pygame.image.load("./images/space_ship.png")
        # create a ship (model) as an object of the class ShipState()
        self._shipmodel = ShipState(310, 460, self._width, 30)

        # load the image of a laser
        self._laserview = pygame.image.load("./images/laser.png")
        # create a list for storing created laser projectiles
        self._lasers = []

        # load the image of an alien
        self._alienview = pygame.image.load("./images/alien.png")
        # create a list for storing created aliens
        self._aliens = []
        # set the number of aliens in a row
        self._numAliens = 7

        # store the time
        self._time = 0
        # store the score
        self._score = 0

        # store the state of the game
        self._running = True
        # store the outcome of the game
        self._win = False

    def rungame(self):
        '''
        Method that behaves as a controller. It is responsible for running the game, taking the user input, 
        validating it and manipulating models.
        It contains infinite loop to maintain the game running.
        '''

        def create_aliens(speed):
            '''
            Method for creating aliens.
            Create a row of aliens by appending created object of class Alien according to given values.
            It takes one parameter - speed, which determines the x and y value of created aliens as well
            as their speed (change of x coordinates of alien)
            '''

            # size of an alien in pixels
            alien_size = 40
            # space between two aliens in pixels
            space_between = 30

            # for loop to create required number of aliens
            for i in range(self._numAliens):
                # if the row is moving to the right = if the change of x coordinates is a positive number
                if speed > 0:
                    # create object of class Alien with required values
                    # and add it at the end of the list storing all created aliens
                    self._aliens.append(AlienState(1 + (space_between + alien_size)*i, 50, self._width, self._height-\
                        80, speed, space_between))
                # if the row is moving to the left = if the change of x coordinates is a negative number
                else:
                    # create object of class Alien with required values
                    # and add it at the end of the list storing all created aliens
                    self._aliens.append(AlienState(self._width - (self._numAliens*(space_between + alien_size)) + space_between +\
                        (space_between + alien_size)*i, 50, self._width, self._height-80, speed, space_between))

        # call the method to create a row of aliens with the speed of 0.05
        create_aliens(0.4)

        # infinite while loop for running the game when self._running is set to True
        while self._running:
            # play background music in a loop
            self._bg_music.play(-1)

            # get the events
            for event in pygame.event.get():
                # if the type of event is QUIT
                if event.type == pygame.QUIT:
                    # raise SystemExit exception and exit Python
                    sys.exit()

                # if the type of event is pressed key
                if event.type == pygame.KEYDOWN:
                    # if the pressed key is left arrow
                    if event.key == pygame.K_LEFT:
                        # call the moveLeft method from our object of a ShipState class
                        # moves the ship to the left in the game
                        self._shipmodel.moveLeft()

                    # if the key is right arrow
                    if event.key == pygame.K_RIGHT:
                        # call the moveRight method from our object of a ShipState class
                        # moves the ship to the right in the game
                        self._shipmodel.moveRight()

                    # if the pressed key is space 
                    if event.key == pygame.K_SPACE:
                        # get the current time 
                        currentTime = pygame.time.get_ticks()

                        # wait 1 second between shooting projectiles
                        # if the current time - time from attribute _time is more than 1 second
                        if currentTime - self._time > 1000:
                            # set the attribute _time to current time to store the time at which 
                            # was the last laser projectile shot
                            self._time = currentTime
                            # create an object of a class Laser and add it to the end of the list storing all shot laser projectiles
                            # set the coordinates according to the ship model and move as needed to center
                            self._lasers.append(LaserState(self._shipmodel.getXPos() + 30, self._shipmodel.getYPos() - 40, 20)) 
                            # play sound effect of shooting on Channel 1 to play multiple sounds at the same time
                            pygame.mixer.Channel(1).play(self._shoot_sound)                     
                
                # if type of event is 'unpressing' the key
                if event.type == pygame.KEYUP:
                    # call the stopMove method from our object of a ShipState class
                    self._shipmodel.stopMove()
            
            # check the length of list storing all created aliens to determine the win
            # if the list storing all created aliens is empty
            if len(self._aliens) == 0:
                # set the attribute _win to True to signalize winning
                self._win = True
                # stop running the game
                self._running = False
                # call the endgame method
                self.endgame()
        
            # draw the screen after handling events
            # set the basic background with the color specified in _black attribute
            self._screen.fill(self._black) 
            # draw the background image
            self._screen.blit(self._bg, (0, 0))
            # draw the ship
            self._screen.blit(self._shipview, (self._shipmodel.getXPos(), self._shipmodel.getYPos()))

            # create text for showing the score
            # True for smooth character edges, rgb code for color and None for transparent background
            self._text = self._font.render('SCORE: ' + str(self._score), True, (255,255,255), None)
            # draw the text
            self._screen.blit(self._text, (10, 10))
            
            # for loop to iterate through the list storing all created laser projectiles
            for laser in self._lasers:
                # call the shoot method from our object's laser's class Laser
                laser.shoot()
                # check if the laser projectile is withing set screen boundaries
                if laser.inScreen() == True:
                    # draw laser projectile
                    self._screen.blit(self._laserview, (laser.getXPos(), laser.getYPos()))
                # if laser projectile out of set screen boundaries
                else:
                    # remove such laser from the list storing all created laser projectiles
                    self._lasers.remove(laser)

            # for loop to iterate through the list storing all created aliens
            for alien in self._aliens:
                # check if alien is within the set screen boundaries
                if alien.withinBordersX() == True:
                    # call the move method from alien's class Alien
                    alien.move()
                    # draw alien
                    self._screen.blit(self._alienview, (alien.getXPos(), alien.getYPos()))

                    # handling collisions
                    # for loop to iterate through the list storing all created laser projectiles
                    for laser in self._lasers:
                        # call the isCollidingWith method from alien's class Alien to check collision with laser projectile
                        if alien.isCollidingWith(laser):
                            # play the sound effect of killing alien on Channel 0 to play multiple sounds at the same time
                            pygame.mixer.Channel(0).play(self._alien_killed_sound)
                            # remove such laser from the list storing all created laser projectiles
                            self._lasers.remove(laser)
                            # remove hit alien from the list storing all created aliens
                            self._aliens.remove(alien)
                            # increment score by 5
                            self._score += 5

                    # call the isCollidingWith method from alien's class Alien to check collision with ship
                    if alien.isCollidingWith(self._shipmodel):
                        # play sound effect of killing player on Channel 0 to play multiple sounds at the same time
                        pygame.mixer.Channel(0).play(self._player_killed_sound)
                        # wait 100 milliseconds
                        pygame.time.wait(100)
                        # set the state of game running to False
                        self._running = False
                        # call endgame method
                        self.endgame()

                    # check if alien reached the set border of the screen
                    if alien.outOfBorderY() == True:
                        # remove such alien from list storing all created aliens
                        self._aliens.remove(alien)

                # if alien reaches the edge of the screen
                else:
                    # change the y coordinates of aliens to move down
                    # iterate through the list storing all created aliens
                    for alien in self._aliens:
                        # call moveDown method from alien's class Alien to change the y coordinates of alien
                        alien.moveDown()
                        # call move method from alien's class Alien to move the alien on the screen
                        alien.move()
                    # create a new row of aliens
                    # call create_aliens method with speed according to already created alien's speed
                    create_aliens(alien.getChange())

            # switch between buffers
            pygame.display.flip()

    def endgame(self):
        '''
        Method for the end state of the game.
        Determines whether the game ended as lost or won and behaves accordingly.
        Behaves also as a controller.
        '''

        # set the background color to color stored in _black attribute
        self._screen.fill(self._black) 
        # draw the background image
        self._screen.blit(self._bg, (0, 0))

        # check the state of the game
        # if _win is set to True
        if self._win == True:
            # create text for winning the game
            # True for smooth character edges, rgb code for color and None for transparent background
            self._wonText = self._font_bigger.render('YOU WON!', True, (255,255,255), None)
            # draw the _wonText
            # extract area that represents the text and set its center to the centre of the screen
            # edit the y coordinate to move it higher
            self._screen.blit(self._wonText, (self._wonText.get_rect(center=(self._width/2, self._height/2 - 25))))
        # if _win is set to False
        else:
            # create text for losing the game
            # True for smooth character edges, rgb code for color and None for transparent background
            self._gameOverText = self._font_bigger.render('GAME OVER', True, (255,255,255), None)
            # draw the _gameOverText
            # extract area that represents the text and set its center to the centre of the screen
            self._screen.blit(self._gameOverText, (self._gameOverText.get_rect(center=(self._width/2, self._height/2 - 25))))

        # create text for showing the final score
        # True for smooth character edges, rgb code for color and None for transparent background
        self._scoreFinal = self._font.render('SCORE: ' + str(self._score), True, (255,255,255), None)
        # draw the _scoreFinal
        # extract area that represents the text and set its center to the centre of the screen
        # edit the y coordinate to move it lower on the screen
        self._screen.blit(self._scoreFinal, (self._scoreFinal.get_rect(center=(self._width/2, self._height/2 + 25))))

        # create text for playing again
        # True for smooth character edges, rgb code for color and None for transparent background
        self._playAgainText = self._font.render('Press space to play again', True, (255,255,255), None)
        # draw the _playAgainText
        # extract area that represents the text and set its center to the centre of the screen
        # edit the y coordinate to move it lower on the screen
        self._screen.blit(self._playAgainText, (self._playAgainText.get_rect(center=(self._width/2, self._height/2 + 150))))

        # switch between buffers
        pygame.display.flip()

        # infinite while loop
        while True:
            # get the events
            for event in pygame.event.get():
                # if the type of event is QUIT
                if event.type == pygame.QUIT:
                    # raise SystemExit exception and exit Python
                    sys.exit()

                # if the type of event is pressed key
                if event.type == pygame.KEYDOWN:
                    # if the pressed key is space
                    if event.key == pygame.K_SPACE:
                        # restart the game
                        # reset the _score value by setting it to 0
                        self._score = 0
                        # reset the _aliens list by making a new empty list
                        self._aliens = []
                        # reset the _lasers list by making a new empty list
                        self._lasers = []
                        # set the state of game in _running to True
                        self._running = True
                        # call the rungame method to run the game 
                        self.rungame()
            

class ShipState(object):
    '''
    Model for Ship.
    State of ship that is being moved based on user interactions.
    Maintains the information that describes the position of the ship, its maximal x coordinate
    and its change of coordinates (speed).
    Contains methods for getting x and y coordinates and handling the movement.
    '''

    # constructor
    def __init__(self, xpos, ypos, maxxpos, change):
        # set the instance attributes
        # x coordinate 
        self._x = xpos
        # y coordinate
        self._y = ypos
        # maximum allowed value for x coordinate
        self._maxX = maxxpos
        # change of the coordinates (speed)
        self._shipChange = change

        # width
        self._width = 75

    def getXPos(self):
        '''
        Getter for x coordinate returning the value of x coordinate of an object.
        '''
        return self._x

    def getYPos(self):
        '''
        Getter for y coordinate returning the value of y coordinate of an object.
        '''
        return self._y

    
    def moveLeft(self):
        '''
        Method for moving object to the left by decrementing its x coordinate.
        Triggered by left arrow in controller.
        '''

        # if the x coordinate - change of coordinates is more than 0 (= is within the screen borders)
        if self._x - self._shipChange > 0:
            # decrement the x coordinate by change of coordinates (speed)
            self._x -= self._shipChange

    def moveRight(self):
        '''
        Method for moving object to the right by incrementing its x coordinate.
        Triggered by right arrow in controller.
        '''
        
        # if the x coordinate + width + change of coordinates is less than maximum allowed value of x coordinate
        if self._x + self._width + self._shipChange < self._maxX:
            # increment the x coordinate by change of coordinates (speed)
            self._x += self._shipChange

    def stopMove(self):
        '''
        Method for stopping the movement of an object.
        Triggered by 'unpressing' the key in controller.
        '''

        # set the x coordinate to itself
        self._x = self._x

class AlienState(object):
    '''
    Model for Alien.
    State of alien that is being moved on the screen.
    Maintains the information that describes the position of the alien, its maximal x and y coordinates,
    its change of coordinates (speed) and the space between two aliens.
    Contains methods for getting x and y coordinates, handling movement, checking whether the coordinates
    are within set boundaries and handling collision
    '''

    # constructor
    def __init__(self, xpos, ypos, maxxpos, maxypos, xchange, space):
        # set instance attributes
        # x coordinate
        self._x = xpos
        # y coordinate
        self._y = ypos
        # maximum allowed value for x coordinate
        self._maxX = maxxpos
        # maximum allowed value for y coordinate
        self._maxY = maxypos
        # change of coordinates (speed)
        self._alienChange = xchange
        # space between two aliens
        self._spaceBetween = space

        # size 
        self._size = 40

    def getXPos(self):
        '''
        Getter for x coordinate returning the value of x coordinate of an object.
        '''
        return self._x

    def getYPos(self):
        '''
        Getter for y coordinate returning the value of y coordinate of an object.
        '''
        return self._y

    def getChange(self):
        '''
        Getter for the change of coordinates returning the value of the change of coordinates of an object.
        '''
        return self._alienChange

    def withinBordersX(self):
        '''
        Method for checking whether the x coordinate is within set boundaries.
        X coordinate cannot be 'out of the screen', therefore lower than 0 and higher than screen's width.
        '''
        
        # check if x coordinate + size + change of coordinates is lower than the maximum allowed x value
        # and if the x coordinate is higher than 0
        if self._x + self._size + self._alienChange < self._maxX and +\
            self._x > 0:
            # return True
            return True 

    def outOfBorderY(self):
        '''
        Method for checking whether the y coordinates are within the set boundaries.
        Alien cannot go below the ship, so the y coordinates cannot be lower than the ship's.
        '''

        # check if y coordinate is higher than the maximum allowed value for y coordinate
        if self._y > self._maxY:
            # return True
            return True

    def move(self):
        '''
        Method for defining the movement of an alien.
        '''
        
        # increment the x coordinate by the change of coordinates (speed)
        self._x += self._alienChange
    
    def moveDown(self):
        '''
        Method for defining the movement downward of an alien.
        Happens when the alien reaches the edge of the screen and has to be moved a row lower.
        '''

        # increment the y coordinate by the size of an alien and the space between two aliens
        self._y += self._size + self._spaceBetween
        # change the direction of alien movement
        # set the change of coordinates to its opposite value
        self._alienChange = -self._alienChange

    def isCollidingWith(self, object):
        '''
        Method for checking the collisions between alien and other object passed in.
        '''

        # calculate the distance between alien and object using mathematical formula
        distance = math.sqrt((math.pow(self._x + self._alienChange -  object.getXPos(), 2)) +
                         (math.pow(self._y -  object.getYPos(), 2)))

        # if the distance is smaller than the size of an alien
        if distance < self._size:
            # return True = collision happened
            return True
        # if the distance is higher than the size of an alien
        else:
            # return False # collision not happening
            return False

    
class LaserState(object):    # model
    '''
    Model for Laser.
    State of laser that is being moved ('shot') on the screen.
    Maintains the information that describes the position of the laser projectile and its change of coordinates (speed).
    Contains methods for getting x and y coordinates, handling movement (shooting), and checking whether the y coordinate
    is within set boundaries.
    The laser projectile shouldn't get 'out of the screen', so its y coordinate can't go under 0.
    '''

    # constructor
    def __init__(self, xpos, ypos, change):
        # set instance attributes
        # x coordinate
        self._x = xpos
        # y coordinate
        self._y = ypos
        # change of coordinates (speed)
        self._laserChange = change

    def getXPos(self):
        '''
        Getter for x coordinate returning the value of x coordinate of an object.
        '''
        return self._x

    def getYPos(self):
        '''
        Getter for y coordinate returning the value of y coordinate of an object.
        '''
        return self._y    

    def inScreen(self):
        '''
        Method for checking whether the y coordinates are within the set boundaries.
        Laser projectile cannot get higher than the upper edge of the screen (0).
        '''

        # check if y coordinate is higher than 0
        if self._y > 0:
            # return True
            return True   

    def shoot(self):
        '''
        Method for 'shooting' the laser projectile. 
        Happens by decrementing the y coordinate to move upwards on the screen.
        Triggered by space in controller.
        '''

        # decrement the y coordinate by the change of coordinates (speed)
        self._y -= self._laserChange 

# execute the game
if __name__ == "__main__":
    # initialize game
    mygame = MyGame()
    # run game
    mygame.rungame()