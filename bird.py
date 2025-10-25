import pygame


class Bird:
    """Clase que representa un pájaro en el juego."""
    
    # Constantes
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.radius = 15  # Radio para colisiones
        
    def jump(self):
        """Hace que el pájaro salte."""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        """Mueve el pájaro aplicando física."""
        self.tick_count += 1
        
        # Fórmula de desplazamiento: d = v*t + 1.5*t^2
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        
        # Velocidad terminal
        if displacement >= 16:
            displacement = 16
            
        if displacement < 0:
            displacement -= 2
            
        self.y = self.y + displacement
        
        # Inclinación del pájaro
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
                
    def draw(self, win):
        """Dibuja el pájaro en la ventana."""
        # Dibujar círculo simple para el pájaro
        pygame.draw.circle(win, (255, 255, 0), (int(self.x), int(self.y)), self.radius)
        # Borde negro
        pygame.draw.circle(win, (0, 0, 0), (int(self.x), int(self.y)), self.radius, 2)
        
    def get_mask(self):
        """Retorna la posición y radio para colisiones."""
        return (int(self.x), int(self.y), self.radius)

