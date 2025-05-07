from setuptools import setup, find_packages

__version__ = "0.0.1"

setup(
    name="cpp_python_demo", # This should match the name in pyproject.toml
    version=__version__,
    author="Demo User",
    author_email="demo@example.com",
    description="A Python library that bundles and compiles its own C++ tools", # Updated description
    long_description="This library provides utilities to compile C++ tools bundled within it.",
    # No C++ extensions for cpp_python_demo itself in this model
    # ext_modules=ext_modules, 
    # cmdclass={"build_ext": build_ext},
    packages=find_packages(where="python_src"), # Find packages in python_src
    package_dir={"": "python_src"},             # Root package is in python_src
    # Ensure that the C++ source files are included in the package
    package_data={
        "cpp_python_demo": ["internal_cpp_sources/*.cpp"],
    },
    include_package_data=True, # Often used with package_data, though MANIFEST.in is more robust for sdists
    zip_safe=False,
    python_requires=">=3.7",
    # Add any runtime dependencies for cpp_python_demo itself here, if any (e.g., "click" for CLI)
    install_requires=[
        # e.g., "shutilwhich>=1.1.0", if you need to ensure compiler existence
    ],
) 