# Python CPU vs. GPU Fractal Generator

This project is a Python-based fractal visualizer designed to serve as a practical demonstration of the performance difference between serial (CPU) and parallel (GPU) computation. The application renders the Mandelbrot set using distinct methods to showcase the power of hardware acceleration.

This project was built to demonstrate a foundational understanding of computer architecture, hardware-software interaction, and professional software development practices.

---

## Features
- **Side-by-Side Benchmark**: A multithreaded application (`benchmark.py`) that runs the CPU and GPU renderers simultaneously to provide a direct, visual comparison of serial vs. parallel performance. Includes performance timers to provide quantitative results.
- **Live CPU Renderer**: A standalone demo (`cpu_demo.py`) that uses multithreading to render the fractal live without freezing the UI, ensuring a responsive user experience.
- **Instant GPU Renderer**: A standalone demo (`gpu_demo.py`) that uses an NVIDIA GPU and a custom CUDA kernel to render the entire fractal almost instantly. The UI is highly efficient, using an event-driven loop to minimize CPU usage.
- **Unit Tested**: Core logic is validated by a suite of unit tests using Python's built-in `unittest` framework.
- **Modular Codebase**: The project is organized with a separation of concerns, with a central `AppState` class for configuration, calculation logic in `engine.py`, and application logic in the demo/benchmark files.

---

## How to Run

### Prerequisites
- Python 3.9 - 3.12 (Officially Supported). Newer versions may work but are not guaranteed.
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
    - For running the application:
        ```bash
        pip install -r requirements.txt
        ```
    - For development (including testing and formatting tools):
        ```bash
        pip install -r requirements-dev.txt
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

### Development Tools
- **Running Tests**:
    ```bash
    python -m unittest discover
    ```
- **Checking Code Formatting**:
    ```bash
    black . --check
    ```
- **Linting Code**:
    ```bash
    ruff check .
    ```

---

## Technologies Used
- **Core**: Python, Pygame, NumPy
- **GPU Acceleration**: CuPy, CUDA (via CuPy RawKernel)
- **Concurrency**: Python's `multithreading` module
- **Testing**: Python's `unittest` framework
- **Code Quality**: Black (formatter), Ruff (linter)
- **Version Control**: Git / GitHub
- **CI/CD**: GitHub Actions, Dependabot