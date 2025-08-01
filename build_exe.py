import PyInstaller.__main__
import os

# Get the current directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the main script path relative to the current directory
main_script = os.path.join(script_dir, 'main.py')

# Define the output directory (dist) and work directory (build)
dist_path = os.path.join(script_dir, 'dist')
build_path = os.path.join(script_dir, 'build')

# Clean up previous build artifacts
if os.path.exists(dist_path):
    import shutil
    shutil.rmtree(dist_path)
if os.path.exists(build_path):
    import shutil
    shutil.rmtree(build_path)

PyInstaller.__main__.run([
    main_script,
    '--onefile',
    '--windowed',
    '--name=ImageMorphPro',
    f'--distpath={dist_path}',
    f'--workpath={build_path}',
    '--noconfirm' # Overwrite previous builds without asking
])
