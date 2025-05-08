import os
import shutil
import setuptools
from setuptools.command.build_py import build_py

# --- Configuration ---
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# Package is now at the root, its name is assumed based on directory
PACKAGE_NAME = 'cpp_python_demo' 
# --- End Configuration ---

class CustomBuildPyCommand(build_py):
    """Custom build command to copy root files into the package build dir."""
    def run(self):
        build_py.run(self)

        platformio_ini_src = os.path.join(PROJECT_ROOT, 'platformio.ini')
        src_dir_src = os.path.join(PROJECT_ROOT, 'src')

        target_dir = None
        if self.build_lib:
            # Construct target path using the package name
            target_dir = os.path.join(self.build_lib, PACKAGE_NAME)
            
        if target_dir and os.path.isdir(target_dir):
            print(f'Custom build: Copying root files to {target_dir}')
            
            if os.path.isfile(platformio_ini_src):
                print(f'  Copying {platformio_ini_src} to {target_dir}')
                shutil.copy(platformio_ini_src, target_dir)
            else:
                print(f'  Warning: {platformio_ini_src} not found, skipping copy.')

            if os.path.isdir(src_dir_src):
                target_src_dir = os.path.join(target_dir, 'src')
                print(f'  Copying directory {src_dir_src} to {target_src_dir}')
                if os.path.exists(target_src_dir):
                    shutil.rmtree(target_src_dir)
                shutil.copytree(src_dir_src, target_src_dir)
            else:
                print(f'  Warning: {src_dir_src} not found, skipping copy.')
        else:
            print('Custom build: Target build directory not found, skipping root file copy.')

# Minimal setup() call
setuptools.setup(
    # Metadata is primarily in pyproject.toml
    # Need packages specified now that find isn't used in pyproject.toml
    packages=[PACKAGE_NAME], 
    cmdclass={
        'build_py': CustomBuildPyCommand,
    },
) 