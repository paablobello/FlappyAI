# Flappy Bird con IA (NEAT)

Implementación de Flappy Bird donde redes neuronales aprenden a jugar usando NEAT (NeuroEvolution of Augmenting Topologies).

## 🎮 ¿Qué hace?

El programa entrena múltiples pájaros simultáneamente usando evolución genética. En cada generación:
- 50 pájaros intentan jugar
- Los que llegan más lejos tienen mejor fitness
- Los mejores se reproducen y mutan
- Después de 10-30 generaciones, aprenden a jugar perfectamente

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
python main.py
```

## 📊 Qué verás en pantalla

- **Gen**: Número de generación actual
- **Vivos**: Cuántos pájaros siguen vivos
- **Score**: Tuberías pasadas en esta generación
- Múltiples pájaros amarillos aprendiendo simultáneamente

## 🧠 Cómo funciona

### Inputs de la red neuronal (3):
1. Posición Y del pájaro
2. Distancia al borde superior de la tubería
3. Distancia al borde inferior de la tubería

### Output (1):
- Si > 0.5 → Saltar
- Si ≤ 0.5 → No hacer nada

### Fitness:
- +0.1 por cada frame que sobrevive
- +5 por cada tubería que pasa
- -1 si choca

## ⚙️ Configuración

Edita `config-neat.txt` para modificar:
- `pop_size`: Pájaros por generación (default: 50)
- `fitness_threshold`: Meta de fitness (default: 10000)
- Tasas de mutación y otros parámetros evolutivos

## 📁 Estructura

```
flappyAI/
├── main.py           # Loop principal con NEAT
├── bird.py           # Clase Bird con física
├── pipe.py           # Clase Pipe con colisiones
├── game.py           # Lógica del juego y rendering
├── config-neat.txt   # Configuración de NEAT
└── requirements.txt  # Dependencias
```

## 💡 Tips

- El entrenamiento es rápido (2-5 minutos normalmente)
- Si no converge, ajusta `weight_mutate_rate` en config-neat.txt
- Presiona cerrar ventana para detener el entrenamiento

