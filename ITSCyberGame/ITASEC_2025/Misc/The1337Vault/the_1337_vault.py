import subprocess
import os
import glob
import shutil
import tempfile

work_dir = os.getcwd()
archives = sorted(glob.glob(os.path.join(work_dir, '*.7z')))
if not archives:
    print('No .7z archive found in the current directory.')
    exit(1)

tmp_dir = tempfile.mkdtemp()
try:
    current_file = shutil.copy(archives[0], tmp_dir)

    layer = None
    try:
        layer = int(os.path.splitext(os.path.basename(current_file))[0].split('_')[-1])
    except Exception:
        layer = None

    while True:
        subprocess.run(['7z', 'x', current_file, f'-o{tmp_dir}', '-y'], capture_output=True)
        os.remove(current_file)

        next_archives = sorted(glob.glob(os.path.join(tmp_dir, '*.7z')))
        if not next_archives:
            for f in os.listdir(tmp_dir):
                if f.endswith('.7z'):
                    continue
                try:
                    with open(os.path.join(tmp_dir, f), 'r', encoding='utf-8') as fh:
                        print(f"Content of {f}:\n{fh.read()}")
                except Exception:
                    pass
            break

        current_file = next_archives[0]
        if layer is not None:
            layer -= 1
finally:
    shutil.rmtree(tmp_dir)
