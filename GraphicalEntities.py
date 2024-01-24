import pygame

class Rectangle:
    def __init__(self, window, x, y, width, height, color):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect)

class TextRectangle(Rectangle):
	def __init__(self, window, x, y, width, height, color, text):
		super().__init__(window, x, y, width, height, color)
		self.text = text
		
	def draw(self):
		super().draw()
		font = pygame.font.Font(None, 16)
		text = font.render(self.text, True, (255,255,255))
		text_rect = text.get_rect(center=self.rect.center)
		self.window.blit(text, text_rect)

class Button(TextRectangle):
	def __init__(self, window, x, y, width, height, color, text):
		super().__init__(window, x, y, width, height, color, text)

	def isClicked(self,mousePos):
		return self.rect.collidepoint(mousePos)

class TextBox(Button):
	pass
