# PiCollision


This is **PiCollision**, a physics simulation of colliding blocks built with Pygame. The project was developed in **2 days** and is inspired by the phenomenal 3Blue1Brown video: [π by Collisions](https://www.youtube.com/watch?v=HEfHFsfGXjs). The simulation visually demonstrates how a series of elastic collisions can reveal digits of π.

<img src="https://github.com/catab60/PiCollision/blob/main/Preview.gif?raw=true" width="800" height="800">

## About the Project

**PiCollision Version 1** focuses on simulating the motion and collisions of two blocks to approximate π. One block represents the smaller mass and the other a much larger mass with a mass ratio based on a power of 100, demonstrating how the number of collisions correlates with the digits of π. The simulation features graphical elements including a real-time collision counter, velocity displays, and a state-space graph to plot block velocities.

### Features:
- **Accurate physics simulation using elastic collisions**
- **Graphical visualization with real-time collision tracking**
- **Interactive controls:** buttons to start/stop or reset the simulation, slider for speed adjustment, and digit control for setting simulation precision.
- **Inspired by 3Blue1Brown's educational video on π and collisions**

## Inspired By:
[![YouTube](http://i.ytimg.com/vi/HEfHFsfGXjs/hqdefault.jpg)](https://www.youtube.com/watch?v=HEfHFsfGXjs)


## Usage Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/catab60/PiCollision.git
   cd PiCollision
   ```
2. **Install the required dependencies:**
   Ensure you have Python and Pygame installed. You can install Pygame using pip:
   ```bash
   pip install pygame
   ```
3. **Run the simulation:**
   ```bash
   python main.py
   ```
4. **Interact with the program:**
   - Use the **Stop/Start** button to pause or resume the simulation.
   - Click **Restart** to reset the simulation.
   - Adjust the **Speed** slider to control the simulation speed.
   - Use the **Digits** control to change the simulation precision (number of π digits computed).

## Learning Experience

Developing PiCollision was an engaging journey into both physics and programming. By simulating the intricate behavior of elastic collisions, I deepened my understanding of mechanics and computational visualization. The project challenged me to balance precision, performance, and visual clarity while staying true to the educational spirit of the inspiring 3Blue1Brown video.

### Contributions

Contributions are welcome! If you notice issues or have ideas for improvements, please feel free to submit a pull request or open an issue in the repository.
