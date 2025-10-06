# Copilot Instructions for the CPU-GPU-Fractal-Generator

## 1. Project Overview

This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance differences between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set using three distinct entry points: a live CPU demo, an instant GPU demo, and a multithreaded benchmark that displays both side-by-side.

The primary goal is to showcase a deep understanding of computer architecture fundamentals, hardware-software interaction, and professional software development practices. The project uses Pygame for the user interface, NumPy for efficient CPU-based array manipulation, and CuPy for GPU-accelerated computing via the NVIDIA CUDA platform.

---

## 2. Core Architecture & Key Files

The project follows a strict **separation of concerns** model. A central `AppState` class manages configuration, a mathematical "engine" is decoupled from the UI, and several application files act as entry points.

* **`state.py` - The Application State Manager**
    This file contains the `AppState` class, which centralizes all rendering parameters (like width, height, and quality) into a single object.

* **`engine.py` - The Calculation & Coloring Engine**
    This module contains all mathematical and coloring logic. It has no knowledge of Pygame and operates on data provided by the application files, often via an `AppState` object.
    * `pixel_to_complex_cpu()`, `calculate_fractal_cpu()`, `colorer_cpu()`: The CPU-based functions that operate on a single coordinate at a time.
    * `calculate_fractal_gpu()`, `colorer_gpu()`: The GPU-based functions that operate on an entire grid of pixels at once.

* **`cpu_demo.py` - The CPU Application Entry Point**
    This script is the user-facing application for the CPU renderer. It is now **multithreaded** to keep the UI responsive, moving the slow, pixel-by-pixel rendering to a background thread.

* **`gpu_demo.py` - The GPU Application Entry Point**
    This script is the user-facing application for the GPU renderer. It pre-renders the image and uses an efficient, **event-driven loop** (`pygame.event.wait()`) to minimize CPU usage while idle.

* **`benchmark.py` - The CPU vs. GPU Benchmark**
    This script is the primary demonstration piece. It uses multithreading to run both renderers simultaneously for a direct, visual performance comparison. It now includes performance timers that print results to the console.

* **`test_engine.py` - Unit Tests**
    This file contains unit tests for the core logic in `engine.py` using Python's built-in `unittest` framework.

---

## 3. Developer Workflows & Configuration

* **To Run the Visualizer:**
    * **CPU Version**: `python cpu_demo.py`
    * **GPU Version**: `python gpu_demo.py`
    * **Benchmark**: `python benchmark.py`

* **To Run Tests:**
    * `python -m unittest discover`

* **To Adjust Quality vs. Speed:**
    * Modify the values passed to the `AppState` constructor in the `main()` function of the respective application file.

---

## 4. Patterns, Conventions, & Dependencies

* **State Management**: The `AppState` class is the single source of truth for rendering parameters. High-level orchestrator functions in the engine should accept the `AppState` object, while low-level pure functions should receive primitive types.
* **Dependencies**: This project requires `pygame`, `numpy`, and `cupy` to run. Development requires `ruff` and `black`.

---

## 5. Recommendations for AI Agents

* **Maintain Separation of Concerns**: Logic belongs in `engine.py`, application flow in the demo/benchmark files, and shared settings in `state.py`.
* **Document Professionally**: All new functions must include a professional docstring explaining their purpose, `Args`, and `Returns`.
* **Respect the Architecture**: The `cpu_demo.py` and `benchmark.py` applications are multithreaded. The `gpu_demo.py` application is event-driven. New features should respect these patterns.

---
*This file should be updated as the project's structure or conventions evolve.*