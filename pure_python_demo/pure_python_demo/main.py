# main.py for pure_python_demo

import os
import sys
# from importlib import resources # Not needed here

try:
    from cpp_python_demo import compile_with_platformio
except ImportError:
    print("Error: Could not import 'compile_with_platformio' from 'cpp_python_demo'.", file=sys.stderr)
    print("Ensure cpp_python_demo is installed and its packaging is correct.", file=sys.stderr)
    sys.exit(1)

def trigger_firmware_compilation():
    print("--- pure_python_demo: Main script started ---")

    # Assuming compile_with_platformio now uses importlib.resources to find its
    # own platformio.ini and src/ within its installation (site-packages).

    # Define where pure_python_demo wants the final firmware
    current_script_path = os.path.abspath(__file__)
    package_dir = os.path.dirname(current_script_path)
    src_root_dir = os.path.dirname(package_dir)
    pure_python_project_root = os.path.dirname(src_root_dir)

    firmware_output_dir = os.path.join(pure_python_project_root, "compiled_firmware_output")
    desired_firmware_filename = "uno_firmware.elf"
    firmware_final_destination = os.path.join(firmware_output_dir, desired_firmware_filename)

    target_environment = "uno_example"

    print(f"Attempting to compile firmware using installed cpp_python_demo (env: '{target_environment}').")
    print(f"Output will be copied to: {firmware_final_destination}")
    
    compiled_firmware_path_at_dest = compile_with_platformio(
        # cpp_project_root_dir is NOT passed.
        environment=target_environment,
        firmware_destination_path=firmware_final_destination,
        verbose=True
    )

    if compiled_firmware_path_at_dest and os.path.exists(compiled_firmware_path_at_dest):
        print(f"Successfully compiled. Firmware is available at: {compiled_firmware_path_at_dest}")
        if compiled_firmware_path_at_dest == firmware_final_destination:
            print(f"Firmware was successfully copied to the desired location in pure_python_demo.")
        else:
            print(f"Firmware was compiled but may not be at the desired pure_python_demo location. Path returned: {compiled_firmware_path_at_dest}")
        print("This firmware is intended for a microcontroller (e.g., Arduino Uno)"
              " and is not directly runnable on this system.")
    else:
        print("Compilation of firmware failed or firmware file not produced/found at destination.")
    
    print("--- pure_python_demo: Main script finished ---")

if __name__ == "__main__":
    trigger_firmware_compilation() 