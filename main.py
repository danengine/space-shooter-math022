import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GROUP 7 - Space Shooter")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.image.load("assets/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
bg_img = pygame.image.load("assets/bg.png")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
explosion_img = pygame.image.load("assets/explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (50, 50))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(1, WIDTH - self.rect.width))
        self.rect.y = random.randint(0, 100) 
        self.speed_x = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x = -self.speed_x

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speed_y = 10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10

        self.glow = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(self.glow, (255, 255, 255, 100), self.glow.get_rect())
        self.glow_rect = self.glow.get_rect(center=self.rect.center)

    def update(self):
        self.rect.y += self.speed_y
        self.glow_rect.center = self.rect.center
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.glow, self.glow_rect)
        surface.blit(self.image, self.rect)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 9:
                self.kill()

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        draw_text2(screen, "GROUP 7 - LINEAR ALGEBRA", 48, WIDTH // 2, HEIGHT // 4 - 50)
        draw_text(screen, "SPACE SHOOTER", 48, WIDTH // 2, HEIGHT // 4 + 50)
        draw_text(screen, "Press any key to start", 22, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                menu_running = False

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("assets/font.ttf", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text2(surf, text, size, x, y):
    font = pygame.font.Font("assets/font2.otf", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press any key to play again", 22, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    global all_sprites, enemies, bullets, enemy_bullets
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create initial enemies
    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Initialize score
    score = 0
    max_enemies = 8  # Maximum number of enemies on the screen

    running = True
    while running:
        pygame.time.Clock().tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for enemy in enemies:
            if random.random() < 0.01:
                enemy.shoot()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for _ in hits:
            score += 10 
            if len(enemies) < max_enemies:
                new_enemy = Enemy()
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            explosion_positions = [
                player.rect.center,
                (player.rect.centerx - 20, player.rect.centery - 20),
                (player.rect.centerx + 20, player.rect.centery + 20)
            ]
            for pos in explosion_positions:
                explosion = Explosion(pos)
                all_sprites.add(explosion)
            player.kill()
            running = False

        screen.blit(bg_img, (0, 0))
        for sprite in all_sprites:
            if isinstance(sprite, Bullet):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)
        draw_text2(screen, f"Score: {score}", 18, WIDTH // 2, 10)
        pygame.display.flip()

    pygame.time.delay(3000)
    game_over_screen()

if __name__ == "__main__":
    while True:
        main_menu()
        main()