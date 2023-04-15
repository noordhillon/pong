# Pong
# A two player graphical pong game.

import pygame


def main():
    # Main function of the program.
    pygame.init()
    pygame.display.set_mode((500, 400))
    pygame.display.set_caption('Pong')   
    w_surface = pygame.display.get_surface() 
    game = Game(w_surface)
    game.play() 
    pygame.quit() 


class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        self.ball = Ball('white', 10, [50, 50], [3, 3], self.surface)
        self.paddle_1 = Paddle(50, 175, 10, 50, self.surface, 'white', 0)
        self.paddle_2 = Paddle(440, 175, 10, 50, self.surface, 'white', 0)
        self.player_1_score = 0
        self.player_2_score = 0

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  
            # Play the game until player clicks close box play frame 
            self.handle_events()
            self.check_collision()
            self.draw()            
            if self.continue_game:
                self.update()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled.
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            if event.type == pygame.KEYUP:
                self.handle_keyup(event)
    
    def handle_keydown(self, event):
        # Handle only the keydown events and change the velocity appropriately.
        # - self is the Game whose events will be handled.
        # - event is the specific event that will be handled. Type = <class 'Event'>
        if event.key == pygame.K_w:
            self.paddle_1.change_velocity('-')
        if event.key == pygame.K_s:
            self.paddle_1.change_velocity('+')
        if event.key == pygame.K_p:
            self.paddle_2.change_velocity('-')
        if event.key == pygame.K_l:
            self.paddle_2.change_velocity('+')
    
    def handle_keyup(self, event):
        # Handle only the keyupevents and change the velocity appropriately.
        # - self is the Game whose events will be handled.
        # - event is the specific event that will be handled. Type = <class 'Event'>        
        if event.key == pygame.K_w or event.key == pygame.K_s:
            self.paddle_1.change_velocity(0)
        if event.key == pygame.K_p or event.key == pygame.K_l:
            self.paddle_2.change_velocity(0)       
    
    def check_collision(self):
        # Checks if the ball has collided with the front side of the padlle and then deflects the ball accordingly.
        # - self is the game whose ball will be deflected.
        if ((self.paddle_1.get_rect().collidepoint(self.ball.get_center())) and (self.ball.get_velocity() < 0)) or ((self.paddle_2.get_rect().collidepoint(self.ball.get_center())) and (self.ball.get_velocity() > 0)):
            self.ball.set_velocity(-1)

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        self.ball.draw()
        self.paddle_1.draw()
        self.paddle_2.draw()
        self.display_score()
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.ball.move()
        self.paddle_1.move()
        self.paddle_2.move()
        self.update_score()
    
    def update_score(self):
        # Updates the score for both the players according to the movement of the ball.
        # - self is the game whose scores will be updated.
        if self.ball.get_center()[0] < 10:
            self.player_2_score = self.player_2_score + 1
        if self.ball.get_center()[0] > 490:
            self.player_1_score = self.player_1_score + 1
        scores = [self.player_1_score, self.player_2_score]
        for score in scores:
            if score > 10:
                self.continue_game = False
    
    def display_score(self):
        # Displays the scores of the two players in the game.
        # - self is the game whose scores will be displayed.
        text_color = pygame.Color('white')        
        text_font = pygame.font.SysFont('', 72)
        score_1 = text_font.render(str(self.player_1_score), True, text_color)
        score_2 = text_font.render(str(self.player_2_score), True, text_color)
        self.surface.blit(score_1, (25,0))
        self.surface.blit(score_2, (450, 0))


class Ball:
    # An object in this class represents a Ball that moves 

    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        # Initialize a Ball.
        # - self is the Ball to initialize
        # - color is the pygame.Color of the ball
        # - center is a list containing the x and y int
        # - coords of the center of the ball
        # - radius is the int pixel radius of the ball
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface

    def move(self):
        # Change the location of the Ball by adding the corresponding.
        # speed values to the x and y coordinate of its center.
        # - self is the Ball.

        for i in range(0,2):
            self.center[i] = self.center[i] + self.velocity[i]
            limit_1 = [490, 390]
            if self.center[i] > limit_1[i] or self.center[i] < 10:
                self.velocity[i] = -self.velocity[i]

    def draw(self):
        # Draw the ball on the surface.
        # - self is the Ball.

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)

    def get_center(self):
        # Returns the coordinates of the center of the ball.
        # - self is the ball whose coordinates will be returned.
        return self.center
    
    def get_velocity(self):
        # Returns the velocity of the ball.
        # - self is the ball whose velocity will be returned.        
        return self.velocity[0]
    
    def set_velocity(self, sign):
        # Sets the velocity of the ball.
        # - selff is the ball whose velocity will be set.
        self.velocity[0] = sign*self.velocity[0]


class Paddle:
    # An object in this class represents a paddle that moves.
    
    def __init__(self, x, y, width, height, surface, color, velocity):
        # Initialises a paddle.
        # - self is the paddle to be initialised.
        # - x is the x coordinate.
        # - y is the y coordinate.
        # - width is the width of the padlle.
        # - height is the height of the padlle.
        # - surface is the surface onto which the padlle will be drawn.
        # - color is the color of the padlle.
        # - velocity is the velocity at which the paddle will move.
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = surface
        self.color = pygame.Color(color)
        self.velocity = velocity
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def change_velocity(self, sign):
        # Change the velocity of the paddle as per the arguments.
        # - self is the paddle whose velocity will be changed.
            if sign == '+' :
                self.velocity = 2
            elif sign == '-' :
                self.velocity = -2
            elif sign == 0:
                self.velocity = 0

    def move(self):
        # Moves the paddle to a new place according to the velocity.
        self.rect.move_ip(0, self.velocity)  # Moves the rectangle without creating a new rectangle.
        self.check_overshoot()
    
    def check_overshoot(self):
        # Checks if the paddle has gone out of the window.
        if self.rect.bottom > 400:
            self.rect.bottom = 400
        if self.rect.top < 0:
            self.rect.top = 0        

    def draw(self):
        # Draws the padlle onto the surface.
        rect = self.rect
        pygame.draw.rect(self.surface, self.color, rect)
    
    def get_rect(self):
        # returns the rectangle(position) of the paddle
        return self.rect


main()