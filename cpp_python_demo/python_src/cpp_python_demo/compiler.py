# cpp_python_demo/python_src/cpp_python_demo/compiler.py

import subprocess
import os
import sys
import shutil
import tempfile

# For Python 3.9+ importlib.resources.files is preferred
# For Python 3.7-3.8, importlib.resources.path is available
# For older versions, pkg_resources or pkgutil would be needed.
# Given python_requires=">=3.7", we can rely on importlib.resources.
from importlib import resources

def find_compiler():
    """Finds a suitable C++ compiler (clang++ or g++)."""
    compilers = ["clang++", "g++"]
    for compiler in compilers:
        if shutil.which(compiler):
            return compiler
    return None

def compile_internal_tool(tool_name: str, output_directory: str, executable_name: str = None, extra_args: list = None) -> str | None:
    """
    Compiles a C++ tool bundled within the library's 'internal_cpp_sources' directory.

    Args:
        tool_name: The name of the C++ source file (without .cpp extension)
                   located in 'internal_cpp_sources'.
        output_directory: Directory where the executable will be placed.
        executable_name: Name for the output executable. If None, defaults to tool_name.
        extra_args: A list of extra arguments to pass to the compiler.

    Returns:
        Absolute path to the compiled executable if successful, None otherwise.
    """
    compiler_exec = find_compiler()
    if not compiler_exec:
        print("Error: No C++ compiler (clang++ or g++) found in PATH.", file=sys.stderr)
        return None

    source_file_name = f"{tool_name}.cpp"
    # The module path for internal_cpp_sources is 'cpp_python_demo.internal_cpp_sources'
    package_name = "cpp_python_demo.internal_cpp_sources"

    try:
        # Using importlib.resources.path to get a file path to the resource.
        # This is a context manager, so the resource is available as a file within the 'with' block.
        # For Python 3.9+, resources.files(package_name).joinpath(source_file_name) is an option too.
        with resources.path(package_name, source_file_name) as source_file_path_cm:
            # source_file_path_cm is a pathlib.Path object
            source_file_path = str(source_file_path_cm) # Convert to string for subprocess

            if not os.path.isfile(source_file_path):
                # This should ideally not happen if resources.path succeeds
                print(f"Error: Internal source file '{source_file_name}' not found after resource lookup.", file=sys.stderr)
                return None

            if not os.path.isdir(output_directory):
                try:
                    os.makedirs(output_directory, exist_ok=True)
                    print(f"Created output directory: {output_directory}")
                except OSError as e:
                    print(f"Error: Could not create output directory {output_directory}: {e}", file=sys.stderr)
                    return None

            if executable_name is None:
                executable_name = tool_name
            
            output_executable_path = os.path.join(output_directory, executable_name)

            compile_command = [
                compiler_exec,
                source_file_path,
                "-o",
                output_executable_path,
                "-std=c++17"  # Default to C++17
            ]

            if extra_args:
                compile_command.extend(extra_args)

            print(f"Attempting to compile internal tool: {' '.join(compile_command)}")

            process = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print(f"Compilation successful. Executable at: {output_executable_path}")
                if stdout:
                    print("Compiler stdout:", stdout)
                return output_executable_path
            else:
                print(f"Error during C++ compilation. Return code: {process.returncode}", file=sys.stderr)
                if stdout:
                    print("Compiler stdout:", stdout, file=sys.stderr)
                if stderr:
                    print("Compiler stderr:", stderr, file=sys.stderr)
                return None
                
    except FileNotFoundError as e:
        # This means the resource (e.g., sample_tool.cpp) was not found by importlib.resources
        print(f"Error: Bundled C++ source file '{source_file_name}' not found in package '{package_name}'. {e}", file=sys.stderr)
        print("Ensure it's included via package_data in setup.py and the package is installed.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during compilation: {e}", file=sys.stderr)
        return None

if __name__ == '__main__':
    print("Testing compiler module (for internal tools)...")
    test_output_dir = os.path.abspath("_test_internal_compile_output")
    
    compiled_tool_path = compile_internal_tool(
        tool_name="sample_tool", 
        output_directory=test_output_dir,
        executable_name="sample_tool_exec"
    )
    
    if compiled_tool_path and os.path.exists(compiled_tool_path):
        print(f"Running compiled internal tool: {compiled_tool_path}")
        try:
            # Ensure executable permissions
            if sys.platform != "win32":
                os.chmod(compiled_tool_path, 0o755)
            result = subprocess.run([compiled_tool_path, "TestArgument"], capture_output=True, text=True, check=True)
            print("Internal tool output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error running internal tool executable:", e.stderr, file=sys.stderr)
        except FileNotFoundError:
            print("Error: Compiled internal tool executable not found or not runnable.", file=sys.stderr)
    else:
        print("Internal tool compilation failed or executable not found.")
    
    # Optional: Clean up test output directory
    # if os.path.exists(test_output_dir):
    #     shutil.rmtree(test_output_dir)
    #     print(f"Cleaned up {test_output_dir}") 