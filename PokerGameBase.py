import pygame


class GameBase:
    def __init__(self, width, height):
        pygame.init()
        self._width = width
        self._height = height

        self._icon = pygame.image.load("Images/pokerchip.png")
        pygame.display.set_icon(self._icon)
        pygame.display.set_caption("Poker")

        self._display = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._framesPerSecond = 30
        self._sprites = pygame.sprite.LayeredUpdates()
        self._ticks = 0
        pygame.key.set_repeat(1, 120)

    def mouseButtonDown(self, x, y):
        return

    def keyDown(self, key):
        return

    def update(self):
        self._sprites.update()

    def draw(self):
        self._sprites.draw(self._display)

    def add(self, sprite):
        self._sprites.add(sprite)

    def getTicks(self):
        return self._ticks

    def quit(self):
        pygame.quit()

    def displayText(self, stringText, x, y, position="center"):
        font = pygame.font.Font("FreeSansBold.ttf", 32)
        text = font.render(stringText, True, [0, 0, 0], [0, 75, 0])
        textRect = text.get_rect()
        if position == "center":
            textRect.center = (x, y)
        if position == "left":
            textRect.x = x
            textRect.y = y
        if position == "right":
            textRect.x = x - textRect.width
            textRect.y = y - textRect.height
        self._display.blit(text, textRect)

    def displayButton(self, text, x, y, boxWidth, boxHeight, action=None):
        font = pygame.font.Font("FreeSansBold.ttf", 25)
        text = font.render(text, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (x + (boxWidth / 2), y - (boxHeight * .75))

        button_color = (0, 75, 0)
        hover_button = (0, 250, 0)

        mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()

        #If the mouse is hovered over the box, then it changes colors
        if x <= mouse[0] <= x + boxWidth and y - boxHeight <= mouse[1] <= y:
            pygame.draw.rect(self._display, hover_button, [x, y - 50, boxWidth, boxHeight])
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and action != None:
            #if click[0] == 1 and action != None:
                    action()
        else:
            pygame.draw.rect(self._display, button_color, [x, y - 50, boxWidth, boxHeight])

        self._display.blit(text, textRect)

    def run(self):
        playing = True
        intro = True
        GREEN = (0, 75, 0)

        while intro:
            self._display.fill(GREEN)
            self.showBank()
            self.displayText("Welcome to Poker, a game of Texas Hold'em!", self._width / 2, self._height - 400)
            self.displayText('Press space to continue', self._width / 2, self._height - 200)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    playing = True
                    intro = False

        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    quit()
            self.update()
            self._display.fill(GREEN)

            pygame.draw.rect(self._display, (0, 0, 0), pygame.Rect(0, 380, 120, 400))
            pygame.draw.rect(self._display, (200, 0, 0), pygame.Rect(280, 380, 230, 150))
            pygame.draw.rect(self._display, (255, 255, 255), pygame.Rect(300, 395, 91, 115), 3)
            pygame.draw.rect(self._display, (255, 255, 255), pygame.Rect(400, 395, 91, 115), 3)

            pygame.draw.rect(self._display, (0, 150, 0), pygame.Rect(110, 215, 91, 115), 3)
            pygame.draw.rect(self._display, (0, 150, 0), pygame.Rect(230, 215, 91, 115), 3)
            pygame.draw.rect(self._display, (0, 150, 0), pygame.Rect(350, 215, 91, 115), 3)
            pygame.draw.rect(self._display, (0, 150, 0), pygame.Rect(470, 215, 91, 115), 3)
            pygame.draw.rect(self._display, (0, 150, 0), pygame.Rect(590, 215, 91, 115), 3)

            self.draw()
            self.showButton()
            self.showPotandBank()

            pygame.display.update()
            self._clock.tick(self._framesPerSecond)
            self._ticks += 1


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__()
        self.loadImage(x, y, filename)

    def loadImage(self, x, y, filename):
        img = pygame.image.load(filename).convert()
        MAGENTA = (255, 0, 255)
        img.set_colorkey(MAGENTA)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height

    def moveBy(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy