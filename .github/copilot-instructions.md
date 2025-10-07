# Copilot Instructions for the CPU-GPU-Fractal-Generator

## 1. Project Overview
This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance differences between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set using three entry points: a live CPU demo, an instant GPU demo, and a multithreaded benchmark that displays both side-by-side.

The primary goal is to showcase a deep understanding of computer architecture fundamentals, hardware-software interaction, and professional software development practices. The project uses Pygame for the user interface, NumPy for efficient CPU-based array manipulation, and CuPy for GPU-accelerated computing via the NVIDIA CUDA platform.

---

## 2. Core Architecture & Key Files
The project follows a strict **separation of concerns** model.

* **`state.py`**: Contains the `AppState` class, which centralizes all rendering parameters (width, height, quality) into a single object.
* **`engine.py`**: The core mathematical "engine," decoupled from the UI. Contains all CPU and GPU calculation and coloring logic.
* **Application Entry Points**:
    * `cpu_demo.py`: Multithreaded application for the responsive CPU renderer.
    * `gpu_demo.py`: Event-driven application for the near-instant GPU renderer.
    * `benchmark.py`: The primary showcase, using multithreading to run both renderers side-by-side for direct comparison.
* **Testing**:
    * `test_engine.py`: Contains unit tests for the core CPU logic in `engine.py`. **Note: GPU functions are not unit tested due to hardware dependencies.**
* **Configuration & Dependencies**:
    * [cite_start]`requirements.txt`: Core dependencies for running the application.
    * [cite_start]`requirements-dev.txt`: Additional dependencies for development, like `black` and `ruff`.
    * `ruff.toml`: Configuration file for the Ruff linter and formatter.

---

## 3. Developer Workflows & Configuration

* **To Run the Visualizer:**
    * **CPU Version**: `python cpu_demo.py`
    * **GPU Version**: `python gpu_demo.py`
    * **Benchmark**: `python benchmark.py`

* **To Run Development Tasks:**
    * **Tests**: `python -m unittest discover`
    * **Linting**: `ruff check .`
    * **Formatting Check**: `black . --check`

---

## 4. Patterns, Conventions, & Dependencies

* **State Management**: The `AppState` class is the single source of truth for rendering parameters.
* **Concurrency**: The `cpu_demo.py` and `benchmark.py` applications are multithreaded. The `gpu_demo.py` application is event-driven. New features should respect these patterns.
* [cite_start]**Dependencies**: Core dependencies are `pygame`, `numpy`, and `cupy`. Development requires `ruff` and `black`.

---

## 5. Recommendations for AI Agents

* **Maintain Separation of Concerns**: Logic belongs in `engine.py`, application flow in the demo/benchmark files, and shared settings in `state.py`.
* **Document Professionally**: All new functions must include a professional docstring explaining their purpose, `Args`, and `Returns`.
* **Adhere to Code Style**: Ensure all new code passes checks from `ruff` and `black` using the project's configuration.
* **Respect the Testing Strategy**: Remember that only CPU-based logic is covered by automated tests.
---
*This file should be updated as the project's structure or conventions evolve.*