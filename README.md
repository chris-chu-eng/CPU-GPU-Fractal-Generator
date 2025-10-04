# Python CPU vs. GPU Fractal Generator

This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance difference between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set using distinct methods to showcase the power of hardware acceleration.

This project was built to demonstrate a foundational understanding of computer architecture, hardware-software interaction, and professional software development practices.

---

## Features
- **Side-by-Side Benchmark**: A multithreaded application (`benchmark.py`) that runs the CPU and GPU renderers simultaneously to provide a direct, visual comparison of serial vs. parallel performance.
- **Live CPU Renderer**: A standalone demo (`cpu_demo.py`) that renders the fractal live, pixel-by-pixel, to visually demonstrate a serial workload.
- **Instant GPU Renderer**: A standalone demo (`gpu_demo.py`) that uses an NVIDIA GPU and a custom CUDA kernel to render the entire fractal almost instantly.
- **Modular Codebase**: The project is organized with a separation of concerns, with calculation logic in `engine.py` and application logic in the demo and benchmark files.

---

## How to Run

### Prerequisites
- Python 3.10 - 3.12 (Officially Supported). Newer versions may work but are not guaranteed.
- An NVIDIA GPU with the CUDA Toolkit installed (required for GPU features).

### Setup
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/chris-chu-eng/CPU-GPU-Fractal-Generator.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd CPU-GPU-Fractal-Generator
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    ```
    - **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    - **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Execution
- To run the primary benchmark comparison:
    ```bash
    python benchmark.py
    ```
- To run the standalone CPU demo:
    ```bash
    python cpu_demo.py
    ```
- To run the standalone GPU demo:
    ```bash
    python gpu_demo.py
    ```

---

## Technologies Used
- **Python**
- **Pygame** (for the user interface)
- **NumPy** (for efficient CPU array creation)
- **CuPy** (for GPU-accelerated operations)
- **CUDA** (for the custom GPU kernel)
- **Multithreading** (for the benchmark application)
- **Git / GitHub** (for version control)
- **GitHub Actions** (for Continuous Integration)