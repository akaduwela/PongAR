# --- Import libraries used for this program
 
import math
import pygame
#import pygame.camera
#from pygame.locals import *
import random
import cv2
import numpy as np

# Define some colors
BLACK = (0 ,0, 0)
WHITE = (255, 255, 255)
 
 
# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Ball(pygame.sprite.Sprite):
 
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        # Create the image of the ball
        self.image = pygame.Surface([10, 10])
 
        # Color the ball
        self.image.fill(WHITE)
 
        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
 
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        # Speed in pixels per cycle
        self.speed = 0
 
        # Floating point representation of where the ball is
        self.x = 0
        self.y = 0
 
        # Direction of ball in degrees
        self.direction = 0
 
        # Height and width of the ball
        self.width = 10
        self.height = 10

        self.score1 = 0
        self.score2 = 0
 
        # Set the initial ball speed and position
        self.reset()
 
    def reset(self):
        self.y = random.randrange(80,400)
        self.x = 300.0
        self.speed=8.0
 
        # Direction of ball (in degrees)
        self.direction = random.randrange(45,135)

        # Flip a 'coin'
        if random.randrange(2) == 0 :
            # Reverse ball direction, let the other guy get it first
            self.direction -= 180
 
    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self,diff):
        self.direction = (360-self.direction)%360
        self.direction -= diff
 
        # Speed the ball up
        self.speed *= 1.1
 
    # Update the position of the ball
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        if self.x < 0:
            self.score1 += 1
            self.reset()
 
        if self.x > 600:
            self.score2 += 1
            self.reset()
 
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 
        # Do we bounce off the top of the screen?
        if self.y <= 30:
            self.direction = (180-self.direction)%360
            #self.x=1
 
        # Do we bounce of the bottom of the screen?
        if self.y > self.screenheight-self.height-30:
            self.direction = (180-self.direction)%360

        return self.rect.y
 
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,pid, y_pos):
        # Call the parent's constructor
        super().__init__()
 
        self.width=15
        self.height=75
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.y = 0
        self.rect.x = y_pos
        self.pid = pid

    # Update the player
    def update(self, newY, ballpos=None):

        if (event.type == pygame.KEYDOWN):
            if (event.key == ord('q')):
                pygame.quit()
     
        # determine from pid if cpu or player.
        # given new paddle midpoint
        # compute distance between ball and midpoint. divide by screen height. alpha value

        if (self.pid == 1):

            a = abs(newY - self.rect.y) / 420

            if (self.rect.y > newY + 40):
                self.rect.y = max(self.rect.y - (a*30), 35)
            elif (self.rect.y < newY - 40):
                self.rect.y = min(self.rect.y + (a*30), 440)

            else:
                self.rect.y = self.rect.y
        else:
            if (self.rect.y > ballpos + 15):
                self.rect.y = max(self.rect.y - 20, 35)
            elif (self.rect.y < ballpos - 15):
                self.rect.y = min(self.rect.y + 20, 440)
            else:
                self.rect.y = self.rect.y 
            # Move x according to the axis. We multiply by 15 to speed up the movement.
        #self.rect.y = newY


        # Make sure we don't push the player paddle off the right side of the screen
        if self.rect.y > self.screenheight - self.height:
            self.rect.y = self.screenheight - self.height


 
score1 = 0
score2 = 0
 
# Call this function so the Pygame library can initialize itself
pygame.init()
#pygame.camera.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([600, 480], pygame.FULLSCREEN)
 
# Set the title of the window
pygame.display.set_caption('Pong')
 
# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)
 
# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
 
# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
 
# Create the ball
ball = Ball()
# Create a group of 1 ball (used in checking collisions)
balls = pygame.sprite.Group()
balls.add(ball)
 
pygame.mixer.music.load('assets/mkmusic.mp3')
pygame.mixer.music.play(-1)

# Create the player paddle object
player1 = Player(0, 580)
player2 = Player(1, 25)
 
movingsprites = pygame.sprite.Group()
movingsprites.add(player1)
movingsprites.add(player2)
movingsprites.add(ball)
 
clock = pygame.time.Clock()
done = False
exit_program = False
 
cam = cv2.VideoCapture(0)

gameStarted = False
start = False
newYprev = 240

screen.fill(BLACK)
while (not start):
    text = font.render("PongAR!", 1, (200, 200, 200))
    textpos = text.get_rect(centerx=background.get_width()/2)
    textpos.top = 50
    screen.blit(text, textpos)

    text2 = font.render("Press 's' to start!", 2, (200, 200, 200))
    textpos2 = text2.get_rect(centerx=background.get_width()/2)
    textpos2.top = 100
    screen.blit(text2, textpos2)

    # Update the screen
    pygame.display.flip()

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == ord('s')):
                start = True


while not exit_program:

    # Clear the screen
    screen.fill(BLACK)

    ret, queryImg = cam.read()

    frame = np.rot90(queryImg)

    Gray= cv2.cvtColor(queryImg, cv2.COLOR_BGR2GRAY)
    Gray= cv2.bilateralFilter(Gray, 11, 17, 17)
    edged = cv2.Canny(Gray, 30, 200)

    edgedRot = np.rot90(edged)

    frame = pygame.surfarray.make_surface(edgedRot)
    screen.blit(frame, (0,0))
 


    # find contours from edged image. If contour is a square, grab that square, find smallest square
    (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea)[-10:]
    screenCnt = None
    flag = False
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if (len(approx) == 4):
            flag = True
            screenCnt = approx
            break
    
    # find vertical position of square
    if (flag):
        newy = (screenCnt[0][0][1] + screenCnt[2][0][1]) / 2
        newYprev = newy
    else:
        newy = newYprev


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
 
    # Stop the game if there is an imbalance of 3 points
    if (ball.score1 == 5) or (ball.score2 == 5):
        done = True
 
    if not done:
        # Update the player and ball positions
        ballpos = ball.update()
        player1.update(newy, ballpos)
        player2.update(newy)
        #ball.update()
 
    # If we are done, print game over
    if done:
        text = font.render("Game Over", 1, (200, 200, 200))
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 50
        screen.blit(text, textpos)
        if (event.type == pygame.KEYDOWN):
            if (event.key == ord('q')):
                pygame.quit()
            elif (event.key == ord('r')):
                done = False
                ball.score1 = 0
                ball.score2 = 0
 
    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player1, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = (player1.rect.y + player1.height/2) - (ball.rect.y+ball.height/2)
 
        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.x = 570
        ball.bounce(-1*diff)
        #hits1 += 1
 
    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player2, balls, False):
        # The 'diff' lets you try to bounce the ball left or right depending where on the paddle you hit it
        diff = (player2.rect.y + player2.height/2) - (ball.rect.y+ball.height/2)
 
        # Set the ball's y position in case we hit the ball on the edge of the paddle
        ball.x = 40
        ball.bounce(diff)
        #hits2 += 1
 

    # Print the score
    scoreprint = str(ball.score2) + " : " + str(ball.score1)
    text = font.render(scoreprint, 1, WHITE)
    textpos = (285, 10)
    screen.blit(text, textpos)
 
 
    # Draw Everything
    movingsprites.draw(screen)
 
    # Update the screen
    pygame.display.flip()
     
    clock.tick(60)
 
pygame.quit()