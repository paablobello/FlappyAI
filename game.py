import pygame
from bird import Bird
from pipe import Pipe


class Game:
    """Clase principal que maneja la lógica del juego."""
    
    WIN_WIDTH = 500
    WIN_HEIGHT = 800
    FLOOR = 730
    
    def __init__(self):
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption("Flappy Bird NEAT")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 30)
        self.score_font = pygame.font.SysFont("arial", 50)
        
    def draw_window(self, birds, pipes, score, gen, alive):
        """Dibuja todos los elementos en la ventana."""
        # Fondo
        self.win.fill((135, 206, 250))  # Azul cielo
        
        # Tuberías
        for pipe in pipes:
            pipe.draw(self.win)
            
        # Suelo
        pygame.draw.rect(self.win, (222, 184, 135), (0, self.FLOOR, self.WIN_WIDTH, 70))
        
        # Pájaros
        for bird in birds:
            bird.draw(self.win)
            
        # Información
        score_text = self.score_font.render(f"Score: {score}", 1, (255, 255, 255))
        self.win.blit(score_text, (self.WIN_WIDTH - score_text.get_width() - 10, 10))
        
        gen_text = self.font.render(f"Gen: {gen}", 1, (255, 255, 255))
        self.win.blit(gen_text, (10, 10))
        
        alive_text = self.font.render(f"Vivos: {alive}", 1, (255, 255, 255))
        self.win.blit(alive_text, (10, 50))
        
        pygame.display.update()
        
    def check_collisions(self, bird, pipes):
        """Verifica colisiones del pájaro."""
        # Colisión con el suelo
        if bird.y + bird.radius >= self.FLOOR:
            return True
            
        # Colisión con el techo
        if bird.y - bird.radius <= 0:
            return True
            
        # Colisión con tuberías
        for pipe in pipes:
            if pipe.collide(bird):
                return True
                
        return False

