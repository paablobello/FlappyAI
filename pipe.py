import pygame
import random


class Pipe:
    """Clase que representa un par de tuberías (superior e inferior)."""
    
    GAP = 150  # Espacio entre tuberías (reducido para más dificultad)
    VEL = 7    # Velocidad de movimiento (aumentado para más dificultad)
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = self.GAP
        
        # Posiciones de las tuberías
        self.top = 0
        self.bottom = 0
        
        self.PIPE_TOP = None
        self.PIPE_BOTTOM = None
        
        self.passed = False
        self.set_height()
        
    def set_height(self):
        """Define la altura aleatoria de las tuberías."""
        self.height = random.randrange(100, 500)
        self.top = self.height - self.PIPE_TOP if hasattr(self, 'PIPE_TOP') and self.PIPE_TOP else self.height
        self.bottom = self.height + self.gap
        
    def move(self):
        """Mueve la tubería hacia la izquierda."""
        self.x -= self.VEL
        
    def draw(self, win):
        """Dibuja las tuberías en la ventana."""
        # Tubería superior
        pygame.draw.rect(win, (0, 255, 0), (self.x, 0, 50, self.height))
        pygame.draw.rect(win, (0, 200, 0), (self.x, 0, 50, self.height), 3)
        
        # Tubería inferior (hasta el suelo en 730)
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.height + self.gap, 50, 730 - self.height - self.gap))
        pygame.draw.rect(win, (0, 200, 0), (self.x, self.height + self.gap, 50, 730 - self.height - self.gap), 3)
        
    def collide(self, bird):
        """Detecta colisión con un pájaro."""
        bird_x, bird_y, bird_radius = bird.get_mask()
        
        # Verificar si el pájaro está en el rango X de la tubería
        if bird_x + bird_radius > self.x and bird_x - bird_radius < self.x + 50:
            # Verificar colisión con tubería superior
            if bird_y - bird_radius < self.height:
                return True
            # Verificar colisión con tubería inferior
            if bird_y + bird_radius > self.height + self.gap:
                return True
                
        return False

