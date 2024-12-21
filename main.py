import pygame
import random

class Ball():
    def __init__(self, case, type, frame_rate):
        self.case = case
        self.type = type
        self.frame = frame_rate/2.5
        self.x2d = 0
        self.y2d = 0
        self.vx = 3
        self.vy = 3
        self.ay = -2
        if self.case == 1:
            self.x = 200+(200/6)
        elif self.case == 2:
            self.x = 300
        elif self.case == 3:
            self.x = 400-(200/6)
        self.y = 200
        self.radius = 10
        self.ball = pygame.Rect((self.x-self.radius, self.y-self.radius), (self.radius, self.radius))
        self.is_alive = True
        self.color = [0, 0, 0]
        
    
    def update(self):
        #Calculateion in 2d plane before projection
        self.x2d += self.vx/self.frame
        self.vy += self.ay/self.frame
        self.y2d += self.vy/self.frame
        
        #Calculation after projection
        magnify = (((350/2.25)/9) * self.x2d) + (50/2.25)
        offset = (200/9)*self.x2d + 200
        if self.case == 1:
            self.x -= ((100+(200/6))/3)/self.frame
        elif self.case == 2:
            pass
        elif self.case == 3:
            self.x += ((100+(200/6))/3)/self.frame
            
        self.y = offset - magnify*self.y2d     
        self.radius += (60/9)/self.frame
        
        if self.type == 1 and self.is_alive:
            self.color[1] = (200/9)*self.x2d
            self.color[2] = (120/9)*self.x2d
        elif self.type == 2 and self.is_alive:
            self.color[0] = (200/9)*self.x2d
            self.color[1] = (50/9)*self.x2d
            

        self.ball = pygame.Rect((self.x-self.radius/2, self.y-self.radius/2), (self.radius, self.radius))
        if self.y > 450:
            self.is_alive = False
        
    def draw(self, screen):
        pygame.draw.ellipse(screen, pygame.Color(self.color), self.ball)
        
        
class Player():
    def __init__(self):
        self.state = 2
        self.player_path = "asset/player.png"
        self.player = pygame.image.load(self.player_path)
        self.x = 225
        self.y = 360
        self.vx = 0
        self.control = True
        
    def shift_left(self):
        if self.state > 1 and self.control:
            self.state -= 1
        
    def shift_right(self):
        if self.state < 3 and self.control:
            self.state += 1
            
    def update(self):
        if self.state == 1 and self.x > 25:
            self.vx = (25 - self.x)/5
        elif self.state == 1:
            self.x = 25
            self.vx = 0
        
        if self.state == 2 and self.x != 225:
            self.vx = (225 - self.x)/5
        elif self.state == 2:
            self.x = 225
            self.vx = 0
        
        if self.state == 3 and self.x < 425:
            self.vx = (425 - self.x)/5
        elif self.state == 3:
            self.x = 425
            self.vx = 0
            
        self.x += self.vx

    def draw(self, screen):
        screen.blit(self.player,(self.x,self.y))
    
class Gamemanager():
    def __init__(self, frame_rate, player):
        self.frame = frame_rate
        self.ball_list = []
        self.gball_list = []
        self.rball_list = []
        self.background_path = "asset/background{:01}.png"
        self.gameover_path = "asset/gameover.png"
        self.score_path = "asset/score.png"
        self.background_list = [pygame.image.load(self.background_path.format(k)).convert() for k in range(1,4)]
        self.background_gameover = pygame.image.load(self.gameover_path)
        self.background_score = pygame.image.load(self.score_path)
        self.background = self.background_list[1]
        self.player = player
        self.player_x = 225
        self.playerrect = pygame.Rect((self.player_x, 395),(150, 20))
        self.score = 0
        self.gameover = False
        self.blitcount = 0
        self.spawn_duration = 100
        self.spawn_cooldown = self.spawn_duration
        self.should_spawn = True
    
    def update(self, player):
        self.player = player
        self.ball_list[:] = [a for a in self.ball_list if a.is_alive]
        self.gball_list[:] = [g for g in self.gball_list if g.is_alive]
        self.rball_list[:] = [r for r in self.rball_list if r.is_alive]
        self.background = self.background_list[self.player.state-1]
        
        self.player_x = player.x
        self.playerrect = pygame.Rect((self.player_x, 395),(150, 20))
        self.blitcount -= 1
        
        if self.should_spawn and not self.gameover:
            self.ball_spawn()
            self.should_spawn = False
        else:
            self.spawn_cooldown -= 1
            
        if self.spawn_cooldown <= 0:
            self.should_spawn = True
            self.spawn_cooldown = self.spawn_duration
            
        if self.spawn_duration > 20:
            self.spawn_duration -= 0.3
        else:
            self.spawn_duration -= 0.003
        
    
    def checkstate(self, screen):
        for g in self.gball_list:
            if g.ball.colliderect(self.playerrect) and g.is_alive:
                g.is_alive = False
                if not self.gameover:
                    self.score += 1
                    self.blitcount = 8
                
        for r in self.rball_list:
            if r.ball.colliderect(self.playerrect) and r.is_alive:
                r.is_alive = False
                self.gameover = True
                self.player.control = False
        
        if self.blitcount > 0:
            screen.blit(self.background_score, (0,0))
        
        if self.gameover:
            screen.blit(self.background_gameover, (0,0))
        
    def ball_spawn(self):
        case = random.randint(1,3)
        type = random.randint(1,2)
        a = Ball(case, type, self.frame)
        if type == 1:
            self.gball_list.append(a)
            self.ball_list.append(a)
        elif type == 2:
            self.rball_list.append(a)
            self.ball_list.append(a)
    
    def display_score(self, screen):
        my_font = pygame.font.SysFont('Century Gothic', 30)
        my_font_sub = pygame.font.SysFont('Century Gothic', 15)
        if not self.gameover:
            score = my_font.render("Score: " + str(self.score), False, (255, 255, 255))
            score_width = score.get_width()
            screen.blit(score, (300-score_width/2,5))
        else:
            gameover = my_font.render("Game Over", False, (255, 150, 150))
            space = my_font_sub.render("Please press the space bar to continue", False, (200, 200, 200))
            score = my_font.render("Score: " + str(self.score), False, (255, 255, 255))
            gameover_width = gameover.get_width()
            space_width = space.get_width()
            score_width = score.get_width()
            
            screen.blit(gameover, (300-gameover_width/2,100))
            screen.blit(space, (300-space_width/2,200))
            screen.blit(score, (300-score_width/2,150))
            
            

def main():
    pygame.init()
    pygame.font.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    frames_per_second = 60
    player = Player()
    game = Gamemanager(frames_per_second, player)
    
    


    while True:
        clock.tick(frames_per_second)

        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.key == pygame.K_LEFT:
                    player.shift_left()
                elif event.key == pygame.K_RIGHT:
                    player.shift_right()
                elif event.key == pygame.K_SPACE and game.gameover:
                    main()
                
        if should_quit:
            break
        
        screen.blit(game.background,(0,0)) 
        player.draw(screen)
        player.update()
        game.update(player)
        
        for a in list(reversed(game.ball_list)):
            a.draw(screen)
            a.update()
        
        game.checkstate(screen)
        game.display_score(screen)
        
        pygame.display.update()
  
    pygame.quit()


if __name__ == "__main__":
    main()