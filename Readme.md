# 🐍 Learn2Slither: Snake AI Game

Este proyecto es una implementación de una **IA para el clásico juego de Snake** usando PyTorch y Pygame. El agente aprende a jugar mediante entrenamiento con aprendizaje por refuerzo. El juego también incluye elementos visuales, modo paso a paso y tipos de comida con efectos diferentes.

---

## 🎮 Características principales

- ⚙️ Entrenamiento del agente mediante Deep Q-Learning (DQN)
- 🧠 Red neuronal simple con una capa oculta (`15 → 512 → 3`)
- 🐍 Jugabilidad clásica de Snake con mecánicas nuevas:
  - Comida verde (+1 punto, +1 tamaño)
  - Comida roja (−1 punto, −1 tamaño)
- 🎮 Se puede jugar al Snake con las teclas de direcciones
  - Guarda las 5 mejores puntuaciones del juego en un json
- 👁️ Modo visual (`-visual on/off`)
- ⏸️ Modo paso a paso (`-step-by-step`)
- 🖼️ Interfaz de configuración opcional con GUI (`-game`)
- 💾 Soporte para guardar y cargar modelos `.pth`

---

## 📦 Estructura del proyecto

```
.
├── snakeAI.py          # Lógica del juego Snake
├── agent.py            # IA basada en DQN
├── model.py            # Red neuronal (PyTorch)
├── train.py            # Punto de entrada (entrenamiento/juego)
├── config_panel.py     # GUI opcional para configuración
├── plot.py             # Visualización de puntuaciones
├── snake_game.py       # Juego de snake para jugar.

```

---

## 🚀 Cómo ejecutar

### Entrenamiento automático:
```bash
python train.py -sessions 100 -visual off
```

### Visualización paso a paso:
```bash
python train.py -step-by-step -speed 10
```

### Con GUI de configuración:
```bash
python train.py -game
```

---

## 🔧 Argumentos útiles

| Argumento        | Descripción                                    |
|------------------|------------------------------------------------|
| `-sessions`      | Número de partidas para entrenar               |
| `-visual`        | `on` o `off` para mostrar u ocultar la ventana |
| `-save`          | Ruta para guardar el modelo `.pth`             |
| `-load`          | Ruta para cargar un modelo `.pth`              |
| `-dontlearn`     | Ejecuta sin entrenamiento                      |
| `-step-by-step`  | Espera pulsación de tecla entre movimientos    |
| `-board-size`    | Tamaño del tablero (10–42)                     |
| `-speed`         | Velocidad del juego (fps)                      |
| `-game`          | Abre la GUI de configuración                   |

---

## 📊 Ejemplo de salida

Durante el entrenamiento, se generan gráficas de progreso usando `matplotlib`, mostrando:

- Puntuaciones por sesión
- Media acumulada

---

## 📥 Requisitos

- Python 3.8+
- PyTorch
- NumPy
- Pygame
- matplotlib

Instalación:
```bash
pip install -r requirements.txt
```

---

## 🧠 Créditos

Este proyecto combina técnicas de IA con mecánicas clásicas del juego Snake para crear una experiencia interactiva y educativa.


[Guía en video sobre el funcionamiento de la red neuronal en el juego snake](https://www.youtube.com/watch?v=VGkcmBaeAGM&list=PLqnslRFeH2UrDh7vUmJ60YrmWd64mTTKV&index=7)

