import pygame
#Perhaps make a Text class that just prints text. incorporate it into textrectangle or something like that
BUTTON_ACTIVE = (229,15,15)
TEXTBOX_ACTIVE = (128,128,128)
ACTIVE_FRAMES = 5

class Rectangle:
    def __init__(self, window, x, y, width, height, color):
        self.window = window
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect)

class TextRectangle(Rectangle):
	def __init__(self, window, x, y, width, height, color, text, fontSize = 25):
		super().__init__(window, x, y, width, height, color)
		self.text = text
		self.fontSize = fontSize
	
	def updateText(self, text):
		self.text = text

	def draw(self):
		super().draw()
		font = pygame.font.Font(None, self.fontSize)
		text = font.render(self.text, True, (255,255,255))
		text_rect = text.get_rect(center=self.rect.center)
		self.window.blit(text, text_rect)

class DummyButton(TextRectangle):
	def __init__(self, window, x, y, width, height, color, text, fontSize = 25):
		super().__init__(window, x, y, width, height, color, text, fontSize)
		self.active = False

	def isClicked(self,mousePos):
		if self.rect.collidepoint(mousePos):
			self.active = True
			return True
		else:
			return False

class Button(DummyButton):
	def __init__(self, window, x, y, width, height, color, text, fontSize = 25):
		super().__init__(window, x, y, width, height, color, text, fontSize)
		self.COLOR_INACTIVE = self.color
		self.frameCounter = 0


	def draw(self):
		self.color = BUTTON_ACTIVE if self.active else self.COLOR_INACTIVE
		if self.active:
			self.frameCounter+=1
			if self.frameCounter == ACTIVE_FRAMES:
				self.frameCounter =0
				self.active = False
		super().draw()

class TextEntryBox(DummyButton):
	def __init__(self,window,x,y,width,height,color,fontSize = 25):
		super().__init__(window,x,y,width,height,color,fontSize=fontSize,text='')
		self.COLOR_INACTIVE = self.color

	def enterText(self,event):
		if self.active:
			if event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
			elif event.key == pygame.K_RETURN:
				text = self.text
				self.text = ''
				self.active = False
				return text
			elif pygame.K_0 <= event.key <= pygame.K_9:
				self.text += event.unicode
		return 0

	def draw(self):
		self.color = TEXTBOX_ACTIVE if self.active else self.COLOR_INACTIVE
		super().draw()

