# Python/C++ Project Setup Demo

This setup demonstrates a way to bundle non-Python project files as installable package data, even when the development layout differs, allowing dependent Python projects to utilize the bundled resources via the installed package. 

It involves two Python projects:

1.  `cpp_python_demo`: A Python package that bundles a C++ project (managed by PlatformIO) and provides a Python function to compile it.
2.  `pure_python_demo`: A Python application that depends on `cpp_python_demo` and uses its compilation function.

The key goal is to show how the C++ project files (`platformio.ini`, `src/`) from `cpp_python_demo` can be packaged and installed into `site-packages` such that `pure_python_demo` can trigger the compilation using the installed version.

## Project Structure

```
setup-demo/                     # Workspace root
├── cpp_python_demo/            # The Python library bundling C++
│   ├── platformio.ini      # PlatformIO config (at root for dev)
│   ├── src/                # C++ source (at root for dev)
│   │   └── main.cpp
│   ├── cpp_python_demo/      # The Python package itself
│   │   ├── __init__.py
│   │   └── compiler.py     # Contains compile_with_platformio
│   ├── pyproject.toml      # Build system definition, project metadata
│   └── setup.py            # Contains custom build logic for installation
└── pure_python_demo/           # Application using the library
    ├── pyproject.toml
    └── pure_python_demo/
        ├── __init__.py
        └── main.py         # Python script using installed cpp_python_demo

```

## Prerequisites

- Python 3.7+
- PlatformIO Core CLI (`pio`) installed and available in your system's `PATH`.
- `uv` (a fast Python package installer and resolver).
- The two project directories (`cpp_python_demo`, `pure_python_demo`) should be siblings.

## How it Works

1.  **`cpp_python_demo` Library**: 
    *   Contains a PlatformIO project (`platformio.ini`, `src/`) at its root.
    *   The Python package `cpp_python_demo` (inside the project) contains `compiler.py` with the function `compile_with_platformio`.
    *   **Packaging**: This is the crucial part.
        *   `setup.py` defines a custom build command (`CustomBuildPyCommand`). 
        *   When `cpp_python_demo` is installed **normally (NOT editable)**, the custom build command runs and copies `platformio.ini` and `src/` from the project root into the package's build directory.
        *   The installation process then places these copied files *inside* the final `site-packages/cpp_python_demo/` directory.
    *   **Execution**: The `compiler.py` (when running from `site-packages`) uses `importlib.resources` to find `platformio.ini` and `src/` right next to it within `site-packages`. It then invokes `pio run` using these bundled files.

2.  **`pure_python_demo` Project**: 
    *   Lists `cpp_python_demo` as a local path dependency in its `pyproject.toml`.
    *   When `pure_python_demo` is installed (using `uv pip install -e .` or `uv pip install .`), `uv` resolves and installs the `cpp_python_demo` dependency **normally** (triggering its custom build).
    *   The `pure_python_demo/main.py` script imports `compile_with_platformio` from the *installed* `cpp_python_demo`.
    *   It calls this function, which then operates on the PlatformIO files within `site-packages/cpp_python_demo/`.
    *   It specifies a destination path within `pure_python_demo` where the final compiled firmware should be copied.

## Installation and Running

1.  **Create a virtual environment for `pure_python_demo`**
    ```bash
    cd /path/to/your/setup-demo/pure_python_demo
    uv venv --python=3.10 .venv 
    source .venv/bin/activate
    ```

2.  **Install `pure_python_demo`**
    Install `pure_python_demo` itself (editably or normally) and crucially, it will resolve the 
    path dependency and perform a **normal install** of `cpp_python_demo`, triggering its custom build step.
    ```bash
    uv pip install -e .
    ```
    *Note: Use `--no-cache-dir` during testing to ensure fresh builds.* 

3.  **Run the `pure_python_demo` main script**
    ```bash
    python pure_python_demo/main.py
    ```

Expected output:
```
--- pure_python_demo: Main script started ---
Attempting to compile firmware using installed cpp_python_demo (env: 'uno_example').
Output will be copied to: /path/to/setup-demo/pure_python_demo/compiled_firmware_output/uno_firmware.elf
Located PlatformIO project resources within installed package at: /path/to/setup-demo/pure_python_demo/.venv/lib/python3.10/site-packages/cpp_python_demo
Attempting to compile PlatformIO project: pio run -d /path/to/setup-demo/pure_python_demo/.venv/lib/python3.10/site-packages/cpp_python_demo -e uno_example --verbose
PlatformIO compilation successful.
...
Original firmware built at: /path/to/setup-demo/pure_python_demo/.venv/lib/python3.10/site-packages/cpp_python_demo/.pio/build/uno_example/firmware.elf
Firmware copied to: /path/to/setup-demo/pure_python_demo/compiled_firmware_output/uno_firmware.elf
Successfully compiled. Firmware is available at: /path/to/setup-demo/pure_python_demo/compiled_firmware_output/uno_firmware.elf
Firmware was successfully copied to the desired location in pure_python_demo.
This firmware is intended for a microcontroller (e.g., Arduino Uno) and is not directly runnable on this system.
--- pure_python_demo: Main script finished ---
```