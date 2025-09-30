# Python CPU vs. GPU Fractal Generator

This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance difference between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set using two distinct methods to showcase the power of hardware acceleration.

This project was built to demonstrate a foundational understanding of computer architecture, hardware-software interaction, and professional software development practices.

---

## Features
- **Dual Renderers**: Includes two separate applications for rendering the Mandelbrot set:
    - `main.py`: A live, pixel-by-pixel renderer that runs on the **CPU**.
    - `main_gpu.py`: A near-instant, pre-rendered version that is accelerated on an **NVIDIA GPU** using CuPy.
- **Modular Codebase**: The project is organized with a separation of concerns, with calculation logic in `engine.py` and application logic in the `main` files.
- **Professional Tooling**: The repository is configured with a `LICENSE`, `dependabot.yml` for automated dependency updates, and a GitHub Actions workflow for Continuous Integration (CI).

---

## How to Run

### Prerequisites
- Python 3.x
- An NVIDIA GPU with the CUDA Toolkit installed (required for `main_gpu.py`).

### Setup
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/chris-chu-eng/CPU-GPU-Fractal-Generator.git](https://github.com/chris-chu-eng/CPU-GPU-Fractal-Generator.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd CPU-GPU-Fractal-Generator
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Execution
- To run the slow, live CPU version:
    ```bash
    python main.py
    ```
- To run the fast, pre-rendered GPU version:
    ```bash
    python main_gpu.py
    ```

---

## Technologies Used
- **Python**
- **Pygame** (for the user interface and display)
- **NumPy** (for efficient CPU array creation)
- **CuPy** (for GPU-accelerated array operations via CUDA)
- **Git / GitHub** (for version control)
- **GitHub Actions** (for Continuous Integration)