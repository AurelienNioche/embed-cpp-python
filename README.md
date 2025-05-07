# Pure Python Demo (Uses cpp_python_demo to Compile Its Bundled C++ Tool)

This project, `pure_python_demo`, demonstrates how to use a separate Python library (`cpp_python_demo`) to compile a C++ tool that is *bundled within* `cpp_python_demo` itself, and then run the resulting executable.

## Project Structure

```
setup-demo/                     # Workspace root
├── cpp_python_demo/            # The Python library for compiling its bundled C++
│   ├── pyproject.toml
│   ├── setup.py
│   └── python_src/cpp_python_demo/
│       ├── __init__.py
│       ├── compiler.py         # Contains C++ compilation logic for internal tools
│       └── internal_cpp_sources/
│           └── sample_tool.cpp # Bundled C++ tool source
└── pure_python_demo/           # This project
    ├── pyproject.toml
    ├── src/
    │   └── pure_python_demo/
    │       ├── __init__.py
    │       └── main.py         # Python script that uses cpp_python_demo
    └── README.md               # This file
```

## Prerequisites

- Python 3.7+
- A C++ compiler (e.g., `clang++` or `g++`) installed and available in your system's PATH.
- `uv` (a fast Python package installer and resolver).
- The `cpp_python_demo` project source code must be present in the directory structure as shown, as `pure_python_demo` depends on it locally.

## How it Works

1.  **`cpp_python_demo` Library**: 
    *   This project is a Python library that now bundles its own C++ source files (e.g., `internal_cpp_sources/sample_tool.cpp`).
    *   Its `setup.py` is configured with `package_data` to ensure these C++ source files are included when `cpp_python_demo` is installed.
    *   The core functionality is in `cpp_python_demo.compiler.compile_internal_tool()`. This function:
        *   Takes the name of an internal tool (e.g., "sample_tool").
        *   Uses `importlib.resources` to locate the corresponding `.cpp` file within the installed `cpp_python_demo` package.
        *   Invokes a system C++ compiler to build an executable from this bundled source.

2.  **`pure_python_demo` Project**: 
    *   Lists `cpp_python_demo` as a local file dependency in its `pyproject.toml`.
    *   When `pure_python_demo` is installed, the `cpp_python_demo` library (including its bundled C++ sources) will also be installed into the same Python environment.
    *   The `pure_python_demo/src/pure_python_demo/main.py` script imports `compile_internal_tool` from `cpp_python_demo`.
    *   It then calls this function, specifying the name of the internal tool it wants to compile (e.g., "sample_tool").
    *   If compilation is successful, `main.py` attempts to run the newly created executable.

## Installation and Running

1.  **Create and Activate a Virtual Environment**
    Navigate to your workspace root (e.g., `setup-demo`):
    ```bash
    uv venv --python=3.10 .venv 
    source .venv/bin/activate
    ```

2.  **Install `pure_python_demo` (which also installs `cpp_python_demo`)**
    Navigate to the `pure_python_demo` directory:
    ```bash
    cd /path/to/your/setup-demo/pure_python_demo
    ```
    Install `pure_python_demo` in editable mode. This will also find and install the local `cpp_python_demo` library from `../cpp_python_demo`:
    ```bash
    uv pip install -e .
    ```

3.  **Run the `pure_python_demo` Main Script**
    This script will trigger the compilation of the C++ tool bundled within the `cpp_python_demo` library.
    ```bash
    python src/pure_python_demo/main.py
    ```

Expected Output (will include compiler messages from `cpp_python_demo`):
```
--- pure_python_demo: Main script started ---
Attempting to compile internal tool 'sample_tool' from cpp_python_demo library...
Attempting to compile internal tool: clang++ /path/to/.venv/lib/python3.10/site-packages/cpp_python_demo/internal_cpp_sources/sample_tool.cpp -o /path/to/setup-demo/pure_python_demo/build_output_internal/sample_tool_app -std=c++17
Compilation successful. Executable at: /path/to/setup-demo/pure_python_demo/build_output_internal/sample_tool_app
Attempting to run the compiled executable...
Output from compiled executable:
Hello from sample_tool (C++)! You passed: FromPurePythonDemo
The sum of 1-5 is 15

--- pure_python_demo: Main script finished ---
```

This setup allows `cpp_python_demo` to act as a self-contained Python library that can deploy and compile its own C++ utility tools on demand when used by another Python project. 