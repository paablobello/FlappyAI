import pygame
import neat
import os
import pickle
import sys
from bird import Bird
from pipe import Pipe
from game import Game

# Variable global para trackear generación
current_generation = 0


def eval_genomes(genomes, config):
    """
    Función de evaluación para NEAT.
    Ejecuta el juego para cada genoma y asigna fitness.
    """
    global current_generation
    current_generation += 1
    
    # Inicializar pygame
    game = Game()
    clock = pygame.time.Clock()
    
    # Crear pájaros y redes neuronales para cada genoma
    birds = []
    nets = []
    ge = []
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)
        
    pipes = [Pipe(600)]
    score = 0
    
    run = True
    while run and len(birds) > 0:
        clock.tick(40)  # Aumentado de 30 a 40 FPS para más velocidad
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        # Determinar qué tubería usar para input de la red
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + 50:
                pipe_ind = 1
                
        # Mover pájaros y dar fitness
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()
            
            # Inputs para la red neuronal
            output = nets[x].activate((
                bird.y,
                abs(bird.y - pipes[pipe_ind].height),
                abs(bird.y - pipes[pipe_ind].bottom)
            ))
            
            # Si el output es > 0.5, saltar
            if output[0] > 0.5:
                bird.jump()
                
        # Verificar colisiones (iterar al revés para poder eliminar)
        for x in range(len(birds) - 1, -1, -1):
            if game.check_collisions(birds[x], pipes):
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        # Mover tuberías
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
                    
            # Verificar si la tubería salió de la pantalla
            if pipe.x + 50 < 0:
                rem.append(pipe)
                
            # Verificar si pasamos la tubería
            if not pipe.passed and pipe.x < birds[0].x if len(birds) > 0 else False:
                pipe.passed = True
                add_pipe = True
                
        # Añadir nueva tubería
        if add_pipe:
            score += 1
            # Bonus de fitness por pasar tubería
            for genome in ge:
                genome.fitness += 5
            pipes.append(Pipe(600))
            
        # Remover tuberías viejas
        for r in rem:
            pipes.remove(r)
            
        # Dibujar ventana
        game.draw_window(birds, pipes, score, current_generation, len(birds))
        
        # Si el score es muy alto, terminar (aumentado para permitir más aprendizaje)
        if score > 100:
            break
            

def run_neat(config_path):
    """Ejecuta NEAT con la configuración especificada."""
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Crear población
    p = neat.Population(config)
    
    # Agregar reporters para ver progreso
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    # Ejecutar fitness function hasta 100 generaciones o fitness objetivo
    winner = p.run(eval_genomes, 100)
    
    # Mostrar el mejor genoma
    print('\n¡Mejor genoma encontrado!\n{!s}'.format(winner))
    
    # Guardar el mejor modelo
    with open('best_bird.pkl', 'wb') as f:
        pickle.dump(winner, f)
    print('\n✅ Modelo guardado en: best_bird.pkl')
    print('💡 Ejecuta "python main.py --play" para ver al mejor pájaro jugar\n')
    
    return winner, config


def play_best(config_path):
    """Carga y ejecuta el mejor modelo guardado."""
    # Verificar si existe el archivo
    if not os.path.exists('best_bird.pkl'):
        print('❌ No se encontró best_bird.pkl')
        print('💡 Primero entrena un modelo con: python main.py --train')
        return
    
    # Cargar el mejor genoma
    with open('best_bird.pkl', 'rb') as f:
        winner = pickle.load(f)
    
    print('\n🎮 Cargando mejor modelo...')
    print(f'Fitness del modelo: {winner.fitness if hasattr(winner, "fitness") else "N/A"}\n')
    
    # Cargar configuración
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Crear red neuronal del mejor genoma
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    
    # Inicializar juego
    game = Game()
    clock = pygame.time.Clock()
    bird = Bird(230, 350)
    pipes = [Pipe(600)]
    score = 0
    
    run = True
    print('🚀 Ejecutando mejor pájaro... (Cierra la ventana para salir)\n')
    
    while run:
        clock.tick(40)
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
                
        # Determinar qué tubería usar para input
        pipe_ind = 0
        if len(pipes) > 1 and bird.x > pipes[0].x + 50:
            pipe_ind = 1
            
        # Mover pájaro
        bird.move()
        
        # Decisión de la IA
        output = net.activate((
            bird.y,
            abs(bird.y - pipes[pipe_ind].height),
            abs(bird.y - pipes[pipe_ind].bottom)
        ))
        
        if output[0] > 0.5:
            bird.jump()
            
        # Verificar colisión primero
        if game.check_collisions(bird, pipes):
            print(f'💀 Game Over! Score final: {score}')
            run = False
            break
        
        # Mover tuberías
        add_pipe = False
        rem = []
        for pipe in pipes:
            pipe.move()
                
            if pipe.x + 50 < 0:
                rem.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            
        for r in rem:
            pipes.remove(r)
            
        # Dibujar (sin mostrar generación, solo el pájaro jugando)
        game.draw_window([bird], pipes, score, "PLAY", 1)
        
    pygame.quit()


if __name__ == '__main__':
    # Inicializar pygame
    pygame.init()
    
    # Ruta al archivo de configuración
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-neat.txt')
    
    # Parsear argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == '--play':
            play_best(config_path)
        elif sys.argv[1] == '--train':
            run_neat(config_path)
        else:
            print('Uso:')
            print('  python main.py --train   # Entrenar nuevo modelo')
            print('  python main.py --play    # Jugar con el mejor modelo')
    else:
        # Por defecto, verificar si existe modelo
        if os.path.exists('best_bird.pkl'):
            print('💡 Modelo encontrado. ¿Qué quieres hacer?')
            print('  python main.py --train   # Entrenar desde cero')
            print('  python main.py --play    # Ver al mejor pájaro jugar\n')
        else:
            print('🎓 Primera vez. Entrenando modelo...\n')
            run_neat(config_path)

