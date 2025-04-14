import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PiCollision")

digits = 2
steps = 10000

class Graph:
    def __init__(self, screen, position, origin, scale, size):
        self.screen = screen
        self.position = position
        self.origin = origin
        self.scale = scale
        self.size = size
        self.surface = pygame.Surface(size)
        self.surface.fill((0, 0, 0))
        self.points_surface = pygame.Surface(size, pygame.SRCALPHA)
        self.points_surface.fill((0, 0, 0, 0))
        self.points = []

    def add_point(self, x, y):
        self.points.append((x, y))
        screen_x = self.origin[0] + x * self.scale
        screen_y = self.origin[1] - y * self.scale
        pygame.draw.circle(self.points_surface, (255, 0, 0), (int(screen_x), int(screen_y)), 3)
        if len(self.points) > 1:
            prev_x, prev_y = self.points[-2]
            prev_screen_x = self.origin[0] + prev_x * self.scale
            prev_screen_y = self.origin[1] - prev_y * self.scale
            pygame.draw.line(
                self.points_surface, (255, 255, 0),
                (int(prev_screen_x), int(prev_screen_y)),
                (int(screen_x), int(screen_y)), 1
            )

    def draw(self):
        self.surface.fill((0, 0, 0))
        for i in range(0, self.size[0], self.scale):
            pygame.draw.line(self.surface, (50, 50, 50), (i, 0), (i, self.size[1]))
        for j in range(0, self.size[1], self.scale):
            pygame.draw.line(self.surface, (50, 50, 50), (0, j), (self.size[0], j))
        pygame.draw.line(self.surface, (255, 255, 255), (0, self.origin[1]), (self.size[0], self.origin[1]), 2)
        pygame.draw.line(self.surface, (255, 255, 255), (self.origin[0], 0), (self.origin[0], self.size[1]), 2)
        self.screen.blit(self.surface, self.position)
        self.screen.blit(self.points_surface, self.position)
        font = pygame.font.Font(None, 20)
        x_label = font.render("x = Red Cube Velocity", True, (255, 255, 255))
        y_label = font.render("y = Green Cube Velocity", True, (255, 255, 255))
        self.screen.blit(x_label, (self.position[0] + 10, self.position[1] + 10))
        self.screen.blit(y_label, (self.position[0] + 10, self.position[1] + 30))

class Block:
    def __init__(self, x, y, width, height, color, velocity, mass, constrain):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)
        self.velocity = velocity
        self.mass = mass
        self.constrain = constrain

    def collide(self, block):
        return not (self.x + self.width < block.x or self.x > block.x + block.width)
    
    def clamp(self, value, min_val, max_val):
        return max(min_val, min(value, max_val))
    
    def bounce(self, block):
        sumMass = self.mass + block.mass
        newVelocity = (self.mass - block.mass)/sumMass * self.velocity + (2 * block.mass / sumMass) * block.velocity
        return newVelocity

    def update(self):
        self.x += self.velocity

    def check_collide_wall(self):
        return self.x <= 20

    def reverse(self):
        self.velocity *= -1

    def draw(self):
        x = self.clamp(self.x, self.constrain, WIDTH)
        self.body = pygame.Rect(x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.body)
        center_x = self.x + self.width // 2
        center_y = self.y - self.height // 2
        text_surface = font.render(f'{self.mass}kg', True, (255, 255, 255))
        screen.blit(text_surface, (center_x - text_surface.get_width() // 2, center_y - text_surface.get_height() // 2))

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(
            text_surface,
            (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
             self.rect.y + (self.rect.height - text_surface.get_height()) // 2)
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, color):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.color = color
        self.handle_rect = pygame.Rect(
            x + (initial_val - min_val) / (max_val - min_val) * width - 5, y - 5, 10, 20
        )
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.x = max(
                self.rect.x, min(event.pos[0] - self.handle_rect.width // 2, self.rect.x + self.rect.width - self.handle_rect.width)
            )
            self.value = self.min_val + (self.handle_rect.x - self.rect.x) / self.rect.width * (self.max_val - self.min_val)

class WarningScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.ok_button = Button(x=450, y=500, width=100, height=50, text="OK", color=(0, 128, 0), text_color=(255, 255, 255))
        self.active = False

    def show(self, message):
        self.message = message
        self.active = True

    def hide(self):
        self.active = False

    def draw(self):
        if self.active:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            text_surface = self.font.render(self.message, True, (255, 0, 0))
            self.screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 50))
            self.ok_button.draw(self.screen)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.ok_button.is_clicked(event.pos):
                self.hide()
                reset_simulation()

font = pygame.font.Font(None, 36)
font1 = pygame.font.Font(None, 44)

warning_screen = WarningScreen(screen, font)

class DigitsControl:
    def __init__(self, x, y, font):
        self.digits = 2
        self.font = font
        self.x = x
        self.y = y
        self.plus_button = Button(x + 160, y, 40, 40, "+", (0, 128, 0), (255, 255, 255))
        self.minus_button = Button(x + 110, y, 40, 40, "-", (128, 0, 0), (255, 255, 255))

    def draw(self, screen):
        self.minus_button.draw(screen)
        self.plus_button.draw(screen)
        digits_text = self.font.render(f"Digits: {self.digits}", True, (255, 255, 255))
        screen.blit(digits_text, (self.x, self.y + 8))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.plus_button.is_clicked(event.pos):
                if self.digits < 6:
                    self.digits += 1
                    reset_simulation()
                else:
                    warning_screen.show("Too many collisions! Max digits = 6.")
            elif self.minus_button.is_clicked(event.pos) and self.digits > 1:
                self.digits -= 1
                reset_simulation()

running = True

block1 = Block(    x=300, y=375, width=50, height=50, color=(0,255,0),     velocity=0, mass=1, constrain=20)
block2 = Block(    x=450, y=350, width=75, height=75, color=(255,0,0),     velocity=-5/steps, mass=pow(100,digits-1), constrain=block1.width+20)
state_space = Graph(screen, position=(20, 462), origin=(257, 257), scale=37, size=(520, 520))

clock = pygame.time.Clock()
sound = pygame.mixer.Sound("clack.wav")
FPS = 60
k = 0

stop_button = Button(x=590, y=770, width=350, height=100, text="Stop", color=(255, 0, 0), text_color=(255, 255, 255))
reset_button = Button(x=590, y=880, width=350, height=100, text="Restart", color=(0, 128, 255), text_color=(255, 255, 255))

speed_slider = Slider(x=680, y=667, width=260, min_val=100, max_val=1, initial_val=5, color=(100, 100, 100))

digits_control = DigitsControl(x=590, y=700, font=font)

simulation_paused = False

def reset_simulation():
    global block1, block2, state_space, k, digits
    digits = digits_control.digits
    block1 = Block(x=300, y=375, width=50, height=50, color=(0,255,0), velocity=0, mass=1, constrain=20)
    block2 = Block(x=450, y=350, width=75, height=75, color=(255,0,0), velocity=-5/steps, mass=pow(100,digits-1), constrain=block1.width+20)
    state_space = Graph(screen, position=(20, 462), origin=(257, 257), scale=37, size=(520, 520))
    k = 0

while running:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255,255,255), (0,425,WIDTH, 20))
    pygame.draw.rect(screen, (255,255,255), (0,0,20, 425))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif warning_screen.active:
            warning_screen.handle_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button.is_clicked(event.pos):
                reset_simulation()
                simulation_paused = False
                stop_button.text = "Stop"
                stop_button.color = (255, 0, 0)
            elif stop_button.is_clicked(event.pos):
                simulation_paused = not simulation_paused
                if simulation_paused:
                    stop_button.text = "Start"
                    stop_button.color = (0, 255, 0)
                else:
                    stop_button.text = "Stop"
                    stop_button.color = (255, 0, 0)
        speed_slider.handle_event(event)
        digits_control.handle_event(event)

    if warning_screen.active:
        warning_screen.draw()
    else:
        if not simulation_paused:
            keys = pygame.key.get_pressed()
            i = 0
            okSound = False
            while i < steps // int(speed_slider.value):
                collision_occurred = False
                if block1.collide(block2):
                    velocity1 = block1.bounce(block2)
                    velocity2 = block2.bounce(block1)
                    block1.velocity = velocity1
                    block2.velocity = velocity2
                    okSound = True
                    k += 1
                    collision_occurred = True

                if block1.check_collide_wall():
                    block1.reverse()
                    okSound = True
                    k += 1
                    collision_occurred = True

                if collision_occurred:
                    mass_ratio = pow(100, digits - 1)
                    normalization_factor = math.sqrt(mass_ratio)
                    x_point = (block2.velocity * steps * math.sqrt(block2.mass)) / normalization_factor
                    y_point = (block1.velocity * steps * math.sqrt(block1.mass)) / normalization_factor
                    state_space.add_point(x_point, y_point)
                    sound.play()

                block1.update()
                block2.update()
                i += 1

        block1.draw()
        block2.draw()
        state_space.draw()

        text = font1.render(f"Collisions: {str(k)}", True, (255, 255, 255))
        screen.blit(text, (590, 500))

        velocity_info_block1 = font.render(
            f"Green Block Velocity: {block1.velocity * 10000:.2f}",
            True, (255, 255, 255)
        )

        velocity_info_block2 = font.render(
            f"Red Block Velocity: {block2.velocity * 10000:.2f}",
            True, (255, 255, 255)
        )

        pi_info = font.render(f"Pi: {math.pi:.6f}", True, (255, 255, 255))

        screen.blit(velocity_info_block1, (590, 580))
        screen.blit(velocity_info_block2, (590, 620))
        screen.blit(pi_info, (590, 540))

        speed_label = font.render("Speed:", True, (255, 255, 255))
        screen.blit(speed_label, (590, 660))

        speed_slider.draw(screen)

        digits_control.draw(screen)

        reset_button.draw(screen)
        stop_button.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()