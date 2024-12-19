import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Frames per second
FPS = 60

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_COLOR = GREEN

# Platform properties
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = BLUE

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Fonts for text rendering
font = pygame.font.SysFont("Arial", 24)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.change_x = 0
        self.change_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False

    def update(self):
        self.calc_gravity()
        self.rect.x += self.change_x

        # Check for screen boundaries
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.y += self.change_y

    def calc_gravity(self):
        if not self.on_ground:
            self.change_y += self.gravity

    def jump(self):
        if self.on_ground:
            self.change_y = self.jump_power
            self.on_ground = False

    def move_left(self):
        self.change_x = -5

    def move_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score = 0
        self.game_over = False

        # Create initial platforms
        self.create_platforms()

    def create_platforms(self):
        for i in range(6):
            x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            y = random.randint(i * 100, i * 100 + 50)
            platform = Platform(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            self.all_sprites.add(platform)
            self.platforms.add(platform)

    def reset_game(self):
        self.__init__()

    def handle_collisions(self):
        player_hit_list = pygame.sprite.spritecollide(self.player, self.platforms, False)

        if player_hit_list:
            for platform in player_hit_list:
                if self.player.change_y > 0:
                    self.player.rect.bottom = platform.rect.top
                    self.player.on_ground = True
                    self.player.change_y = 0

    def run_logic(self):
        if not self.game_over:
            self.all_sprites.update()
            self.handle_collisions()

            # Check if player falls below the screen
            if self.player.rect.top > SCREEN_HEIGHT:
                self.game_over = True

    def display_frame(self):
        screen.fill(WHITE)

        if self.game_over:
            self.display_game_over()
        else:
            self.all_sprites.draw(screen)

            # Display score
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def display_game_over(self):
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

# Main function
def main():
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.player.move_left()
                if event.key == pygame.K_RIGHT:
                    game.player.move_right()
                if event.key == pygame.K_SPACE:
                    game.player.jump()
                if event.key == pygame.K_r and game.game_over:
                    game.reset_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    game.player.stop()

        game.run_logic()
        game.display_frame()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
