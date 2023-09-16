import pygame 
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/2.png').convert_alpha()
        player_walk_3 = pygame.image.load('graphics/player/3.png').convert_alpha()
        player_walk_4 = pygame.image.load('graphics/player/4.png').convert_alpha()
        player_walk_5 = pygame.image.load('graphics/player/5.png').convert_alpha()
        player_walk_6 = pygame.image.load('graphics/player/6.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2,player_walk_3,player_walk_4,player_walk_5,player_walk_6]
        self.player_index = 0
        self.player__jump = pygame.image.load('graphics/jump/1.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/cartoon_jump.mp3')
        self.jump_sound.set_volume(0.5)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player__jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update (self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'crab':
            crab_1 = pygame.image.load('graphics/enemy2/1.png').convert_alpha()
            crab_2 = pygame.image.load('graphics/enemy2/2.png').convert_alpha()
            crab_3 = pygame.image.load('graphics/enemy2/3.png').convert_alpha()
            crab_4 = pygame.image.load('graphics/enemy2/4.png').convert_alpha()
            crab_5 = pygame.image.load('graphics/enemy2/5.png').convert_alpha()
            crab_6 = pygame.image.load('graphics/enemy2/6.png').convert_alpha()
            self.frames = [crab_1,crab_2,crab_3,crab_4,crab_5,crab_6]
            y_pos = 300
        else:
            shell_1 = pygame.image.load('graphics/enemy1/1.png').convert_alpha()
            shell_2 = pygame.image.load('graphics/enemy1/2.png').convert_alpha()
            shell_3 = pygame.image.load('graphics/enemy1/3.png').convert_alpha()
            shell_4 = pygame.image.load('graphics/enemy1/4.png').convert_alpha()
            shell_5 = pygame.image.load('graphics/enemy1/5.png').convert_alpha()
            self.frames = [shell_1,shell_2,shell_3,shell_4,shell_5]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            

def display_score():
    current_time = int(pygame.time.get_ticks() /1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(shell_surf, obstacle_rect)
            else: screen.blit(crab_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x>-100]
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom <300:
        player_surf = player__jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400 ))
pygame.display.set_caption('Pirates') 
clock = pygame.time.Clock()
test_font = pygame.font.Font('graphics/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/bg1.mp3')
bg_music.set_volume(1)
bg_music.play(loops = -1)

#groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface_frame = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

#shell
shell_frame_1 = pygame.image.load('graphics/enemy1/1.png').convert_alpha()
shell_frame_2 = pygame.image.load('graphics/enemy1/2.png').convert_alpha()
shell_frame_3 = pygame.image.load('graphics/enemy1/3.png').convert_alpha()
shell_frame_4 = pygame.image.load('graphics/enemy1/4.png').convert_alpha()
shell_frame_5 = pygame.image.load('graphics/enemy1/5.png').convert_alpha()
shell_frames = [shell_frame_1,shell_frame_2,shell_frame_3,shell_frame_4,shell_frame_5]
shell_frame_index = 0
shell_surf = shell_frames[shell_frame_index]

#crab
crab_frame_1 = pygame.image.load('graphics/enemy2/1.png').convert_alpha()
crab_frame_2 = pygame.image.load('graphics/enemy2/2.png').convert_alpha()
crab_frame_3 = pygame.image.load('graphics/enemy2/3.png').convert_alpha()
crab_frame_4 = pygame.image.load('graphics/enemy2/4.png').convert_alpha()
crab_frame_5 = pygame.image.load('graphics/enemy2/5.png').convert_alpha()
crab_frame_6 = pygame.image.load('graphics/enemy2/6.png').convert_alpha()
crab_frames = [crab_frame_1,crab_frame_2,crab_frame_3,crab_frame_4,crab_frame_5,crab_frame_6]
crab_frame_index = 0
crab_surf = crab_frames[crab_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/2.png').convert_alpha()
player_walk_3 = pygame.image.load('graphics/player/3.png').convert_alpha()
player_walk_4 = pygame.image.load('graphics/player/4.png').convert_alpha()
player_walk_5 = pygame.image.load('graphics/player/5.png').convert_alpha()
player_walk_6 = pygame.image.load('graphics/player/6.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2,player_walk_3,player_walk_4,player_walk_5,player_walk_6]
player_index = 0
player__jump = pygame.image.load('graphics/jump/1.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (800,300))
player_gravity = 0

#intro screen
player_stand = pygame.image.load('graphics/jump/1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pirates',False,(111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = test_font.render('Press space to run',False,(111,196,169))
game_message_rect=game_message.get_rect(center= (400,320))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

shell_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(shell_animation_timer,1500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >=300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >=300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key ==pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['crab','shell','shell','shell'])))

                if event.type == shell_animation_timer:
                    if shell_frame_index == 0: shell_frame_index = 1
                    shell_surf = shell_frame[shell_frame_index]

                if event.type == fly_animation_timer:
                    if crab_frame_index == 0: crab_frame_index = 1
                    crab_surf = crab_frame[crab_frame_index]
        
    if game_active:
        screen.blit(sky_surface_frame,(0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score:{score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,300))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)
    pygame.display.update()
    clock.tick(60)