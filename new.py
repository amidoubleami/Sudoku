import pygame
import pygame.gfxdraw

# Initialize Pygame
pygame.init()

# Set up the display window
window_width, window_height = 400, 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Button Grid Example")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the Button class
class Button:
    def __init__(self, x, y, width, height, color, number):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.number = number

    def draw(self):
        pygame.gfxdraw.box(window, self.rect, self.color)
        self.draw_number()

    def draw_number(self):
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.number), True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        window.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                display_number(self.number)

# Display the number in the window
def display_number(number):
    pygame.draw.rect(window, WHITE, (150, 150, 100, 100))  # Clear the display area
    font = pygame.font.Font(None, 100)
    text = font.render(str(number), True, BLACK)
    text_rect = text.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(text, text_rect)

# Create Button instances
button_width, button_height = 30,30
button_padding = 5
button_radius = 100

buttons = []
for i in range(3):
    for j in range(3):
        x = j * (button_width + button_padding) + button_padding
        y = i * (button_height + button_padding) + button_padding
        number = i * 3 + j + 1
        button = Button(x, y, button_width, button_height, RED, number)
        buttons.append(button)

# Game loop
running = True
while running:
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    # Draw the buttons
    for button in buttons:
        button.draw()

    pygame.display.update()

# Quit Pygame
pygame.quit()

