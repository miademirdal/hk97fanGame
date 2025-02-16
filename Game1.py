import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 7
SPAWN_RATE = 0.02

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hong Kong 97 fan game")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        # Update position based on speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # If enemy goes off screen, respawn at top
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -BULLET_SPEED

    def update(self):
        self.rect.y += self.speedy
        # Kill bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Game:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Initialize score
        self.score = 0
        self.game_over = False

    def spawn_enemy(self):
        if random.random() < SPAWN_RATE:
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.shoot()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        
        # Get pressed keys for continuous movement
        keys = pygame.key.get_pressed()
        self.player.speed_x = 0
        self.player.speed_y = 0
        if keys[pygame.K_LEFT]:
            self.player.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.player.speed_x = PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.player.speed_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.player.speed_y = PLAYER_SPEED
        
        return True

    def shoot(self):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

    def check_collisions(self):
        # Check for collisions between bullets and enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for hit in hits:
            self.score += 1
        
        # Check for collisions between player and enemies
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.game_over = True

    def update(self):
        if not self.game_over:
            self.spawn_enemy()
            self.all_sprites.update()
            self.check_collisions()

    def draw(self):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render('YOU IS DEAD', True, WHITE)
            restart_text = self.font.render('Press R to restart', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))
        
        pygame.display.flip()

def main():
    game = Game()
    running = True
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
