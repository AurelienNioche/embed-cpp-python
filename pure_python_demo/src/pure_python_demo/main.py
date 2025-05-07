# main.py for pure_python_demo

import os
import sys
import subprocess

# Attempt to import the compiler function from cpp_python_demo
# This relies on cpp_python_demo being installed in the environment
# (e.g., via 'uv pip install -e .' in pure_python_demo directory,
# which installs cpp_python_demo due to the dependency in pyproject.toml)
try:
    from cpp_python_demo import compile_internal_tool
except ImportError:
    print("Error: Could not import 'compile_internal_tool' from 'cpp_python_demo'.", file=sys.stderr)
    print("Please ensure cpp_python_demo is installed correctly.", file=sys.stderr)
    print("Try running 'uv pip install -e .' in the 'pure_python_demo' directory.", file=sys.stderr)
    sys.exit(1)

def run_internal_tool_compilation_and_execute():
    print("--- pure_python_demo: Main script started ---")

    # Define where the compiled output should go
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    output_build_dir = os.path.abspath(os.path.join(current_script_dir, "..", "..", "build_output_internal"))
    tool_to_compile = "sample_tool" # This is the name of the .cpp file in cpp_python_demo's internal_cpp_sources

    print(f"Attempting to compile internal tool '{tool_to_compile}' from cpp_python_demo library...")
    
    compiled_executable_path = compile_internal_tool(
        tool_name=tool_to_compile,
        output_directory=output_build_dir,
        executable_name=f"{tool_to_compile}_app" # Custom name for the output executable
    )

    if compiled_executable_path and os.path.exists(compiled_executable_path):
        print(f"Successfully compiled. Executable is at: {compiled_executable_path}")
        print("Attempting to run the compiled executable...")
        try:
            if sys.platform != "win32":
                os.chmod(compiled_executable_path, 0o755)
            
            # Pass an argument to the sample_tool
            result = subprocess.run([compiled_executable_path, "FromPurePythonDemo"], capture_output=True, text=True, check=True)
            print("Output from compiled executable:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running compiled executable. Return code: {e.returncode}", file=sys.stderr)
            print(f"Stdout: {e.stdout}", file=sys.stderr)
            print(f"Stderr: {e.stderr}", file=sys.stderr)
        except FileNotFoundError:
            print(f"Error: Compiled executable not found at {compiled_executable_path} or not runnable.", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred while running the executable: {e}", file=sys.stderr)
    else:
        print("Compilation of internal tool failed or executable not produced.")
    
    print("--- pure_python_demo: Main script finished ---")

if __name__ == "__main__":
    run_internal_tool_compilation_and_execute() 