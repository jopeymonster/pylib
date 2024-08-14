import subprocess

def install_package(package):
    try:
        # Try installing the package with pip
        subprocess.check_call(["pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Skipping {package} as it could not be installed.")

# Open and read the requirements.txt file (or change)
with open("requirements.txt", "r") as file:
    packages = file.readlines()

# Install each package individually
for package in packages:
    package = package.strip()
    if package:  # Only attempt to install non-empty lines
        print(f"Installing {package}...")
        install_package(package)
