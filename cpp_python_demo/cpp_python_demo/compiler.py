# cpp_python_demo/python_src/cpp_python_demo/compiler.py

import subprocess
import os
import sys
import shutil
from importlib import resources

def compile_with_platformio(
    environment: str = None,
    output_firmware_name: str = "firmware",
    firmware_destination_path: str = None,
    verbose: bool = False
) -> str | None:
    """
    Compiles the PlatformIO project using resources bundled with the package.
    Assumes platformio.ini and src/ have been installed into the package dir.

    Args:
        environment: The PlatformIO environment to build.
        output_firmware_name: Base name of the expected firmware file.
        firmware_destination_path: If provided, copy firmware to this full path.
        verbose: If True, prints more detailed output.

    Returns:
        Absolute path to the final firmware, or None on failure.
    """
    try:
        # Find the installed package path using platformio.ini as a resource
        # This requires platformio.ini to be correctly installed as package data.
        with resources.path('cpp_python_demo', 'platformio.ini') as pio_ini_cm_path:
            # The directory containing platformio.ini is the project dir for PlatformIO
            project_dir = str(pio_ini_cm_path.parent) 
            pio_ini_path = str(pio_ini_cm_path)
        
        print(f"Located PlatformIO project resources within installed package at: {project_dir}")

        # Sanity check paths derived from resource finding
        if not os.path.isfile(pio_ini_path):
            # This shouldn't happen if resources.path succeeded, but check anyway
            print(f"Error: platformio.ini resource found by importlib but not a file at: {pio_ini_path}?", file=sys.stderr)
            return None
        
        src_dir_path = os.path.join(project_dir, "src")
        if not os.path.isdir(src_dir_path):
            print(f"Error: src/ directory not found within installed package at: {src_dir_path}", file=sys.stderr)
            print("Ensure cpp_python_demo's setup/packaging installs src/ correctly.", file=sys.stderr)
            return None

        pio_command = ["pio", "run", "-d", project_dir]
        
        actual_env_to_check = environment
        if environment:
            pio_command.extend(["-e", environment])
        else:
            print("No environment specified, relying on default_envs in platformio.ini.")
            with open(pio_ini_path, 'r') as f:
                for line in f:
                    if line.strip().startswith("default_envs ="):
                        actual_env_to_check = line.split('=')[1].strip().split(',')[0]
                        break
                else:
                    print("Warning: Could not determine default_envs from platformio.ini...", file=sys.stderr)
                    actual_env_to_check = None 
            if actual_env_to_check and actual_env_to_check != environment:
                 print(f"Using default environment from platformio.ini: {actual_env_to_check}")
                 if actual_env_to_check: 
                      pio_command.extend(["-e", actual_env_to_check])
            elif not actual_env_to_check and environment:
                 actual_env_to_check = environment 

        if verbose:
            pio_command.append("--verbose")

        print(f"Attempting to compile PlatformIO project: {' '.join(pio_command)}")

        process = subprocess.Popen(pio_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("PlatformIO compilation successful.")
            if verbose and stdout:
                print("PlatformIO stdout:\n", stdout)

            current_env_for_path = actual_env_to_check if actual_env_to_check else environment
            if not current_env_for_path:
                 print("Error: No specific environment was built...", file=sys.stderr)
                 return None

            firmware_dir_pio = os.path.join(project_dir, ".pio", "build", current_env_for_path)
            source_firmware_elf_path = os.path.join(firmware_dir_pio, f"{output_firmware_name}.elf")
            source_firmware_hex_path = os.path.join(firmware_dir_pio, f"{output_firmware_name}.hex")
            
            final_firmware_path_in_pio = None
            if os.path.exists(source_firmware_elf_path):
                final_firmware_path_in_pio = os.path.abspath(source_firmware_elf_path)
            elif os.path.exists(source_firmware_hex_path):
                final_firmware_path_in_pio = os.path.abspath(source_firmware_hex_path)
            
            if not final_firmware_path_in_pio:
                print(f"Error: Compiled firmware ('{output_firmware_name}.elf/hex') not found...", file=sys.stderr)
                print(f"Looked in: {firmware_dir_pio}", file=sys.stderr)
                return None
            
            print(f"Original firmware built at: {final_firmware_path_in_pio}")

            if firmware_destination_path:
                try:
                    dest_dir = os.path.dirname(firmware_destination_path)
                    if dest_dir: 
                        os.makedirs(dest_dir, exist_ok=True)
                    shutil.copy(final_firmware_path_in_pio, firmware_destination_path)
                    print(f"Firmware copied to: {firmware_destination_path}")
                    return os.path.abspath(firmware_destination_path)
                except Exception as e_copy:
                    print(f"Error copying firmware to {firmware_destination_path}: {e_copy}", file=sys.stderr)
                    return final_firmware_path_in_pio 
            else:
                return final_firmware_path_in_pio
        else:
            print(f"Error during PlatformIO compilation...", file=sys.stderr)
            if stdout:
                print("PlatformIO stdout:", stdout, file=sys.stderr)
            if stderr:
                print("PlatformIO stderr:", stderr, file=sys.stderr)
            return None

    except FileNotFoundError as e:
        if e.__class__.__name__ == 'FileNotFoundError' and hasattr(e, 'filename') and e.filename and 'platformio.ini' in e.filename:
             # This error now means platformio.ini wasn't found *as a package resource*
             print(f"Error: 'platformio.ini' not found as a resource in the installed 'cpp_python_demo' package. {e}", file=sys.stderr)
             print("Ensure cpp_python_demo's setup/packaging correctly installs it as package data.", file=sys.stderr)
        elif "pio" in str(e).lower() or (e.filename and "pio" in e.filename.lower()):
             print(f"Error: PlatformIO command ('pio') not found. {e}", file=sys.stderr)
        else:
            print(f"An unexpected FileNotFoundError occurred: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred during PlatformIO compilation: {e}", file=sys.stderr)
        return None

if __name__ == '__main__':
    # This block might fail if run directly from source tree,
    # as it now relies on the package being installed so importlib.resources works.
    target_environment = "uno_example" 
    print(f"\nAttempting to compile environment '{target_environment}' using installed package resources.")

    firmware_path = compile_with_platformio(
        environment=target_environment,
        verbose=True
    )
    if firmware_path:
        print(f"Successfully compiled. Firmware available at: {firmware_path}")
    else:
        print("PlatformIO compilation failed for the self-test.")
