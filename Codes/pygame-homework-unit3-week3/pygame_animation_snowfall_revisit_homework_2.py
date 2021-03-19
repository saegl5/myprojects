import pygame, random
pygame.init()
 
WHITE = pygame.Color("white")
CYAN = pygame.Color("cyan")
BLACK = pygame.Color("black")

size = (704, 512)
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()
background_image = pygame.image.load("winter.jpeg") # background image from https://unsplash.com/photos/kVKz9qnJC-k, see License.txt
snowflakes = []
i = int()
r = 4

pygame.display.set_caption("QUESTABOX's Cool Animation")

for i in range(0, 50):
    x = random.randrange(0, size[0]+1)
    y = random.randrange(0, size[1]+1)
    snowflakes.append((x, y))
    snowflakes[i] = list(snowflakes[i])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        else:
            None
    screen.blit(background_image, (0, 0))

    # --- Challenge
    pygame.draw.rect(screen, CYAN, (100, 300, 200, 100), width=0)
    pygame.draw.line(screen, CYAN, (100, 300), (100, 512), width=5)
    font = pygame.font.SysFont('Arial', 25, bold=True, italic=False) # (font family, size [pixels], bold, italics)
    text = font.render("Welcome!", True, BLACK) # (string, anti-aliased [i.e., thin and smooth], color)
    screen.blit(text, (135, 335)) # (image, position)
    # ---
    
    for i in range(0, len(snowflakes)):
        pygame.draw.circle(screen, WHITE, snowflakes[i], radius=r, width=0)
        snowflakes[i][1] += 1
        if snowflakes[i][1] > size[1]+r:
            snowflakes[i][1] = random.randrange(-50, -r)
            snowflakes[i][0] = random.randrange(0, size[0]+1)
        else:
            None
    pygame.display.flip()
    clock.tick(60)
pygame.quit()