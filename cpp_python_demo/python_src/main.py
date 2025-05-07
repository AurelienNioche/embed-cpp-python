# This script demonstrates how to use the C++ extension module.

# After building the project (e.g., with 'pip install .'),
# the 'cpp_module' will be available for import.

try:
    import cpp_module
except ImportError as e:
    print("Error importing cpp_module. Please ensure the project is built and installed.")
    print(f"Details: {e}")
    # You might need to add the build directory to sys.path if running without installation
    # For example, if 'cpp_module.cpython-3XX-darwin.so' is in a 'build' subdirectory:
    # import sys
    # import os
    # sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'build', 'lib.macosx-10.9-x86_64-cpython-39')) # Adjust path as needed
    # import cpp_module
    exit(1)

def run_demo():
    # Test the greet function
    message = cpp_module.greet("Python User")
    print(f"From C++ greet function: {message}")

    # Test the version attribute
    print(f"C++ module version: {cpp_module.__version__}")

    # Test the Calculator class
    calc = cpp_module.Calculator(10)
    print(f"Initial calculator value: {calc.get_value()}")

    calc.add(5)
    print(f"After adding 5: {calc.get_value()}")

    calc.subtract(3)
    print(f"After subtracting 3: {calc.get_value()}")

    calc2 = cpp_module.Calculator() # Uses default constructor value
    print(f"Calculator 2 initial value: {calc2.get_value()}")
    calc2.add(100)
    print(f"Calculator 2 after adding 100: {calc2.get_value()}")

if __name__ == "__main__":
    run_demo() 