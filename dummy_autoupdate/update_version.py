import subprocess
import sys
import logging
from pathlib import Path


def update_version(package: str = 'dummy_autoupdate', version: str = None,
                   num_of_attempts: int = 3) -> bool:
    logger = logging.getLogger(__name__)

    if version:
        package = f'{package}=={version}'

    logger.info(f'Updating package {package}')

    executable: str = sys.executable

    if executable.endswith('pythonw.exe'):
        logger.info(f'Executable is pythonw.exe: {executable}.')
        p = Path(executable).parent / 'python.exe'
        if p.is_file():
            executable = str(p.resolve())
        else:
            logger.info(f'No python.exe interpreter found.')
            return False

    CREATE_NO_WINDOW = 0x08000000

    for i in range(num_of_attempts):
        try:
            logger.info(f'Updating the package with {executable} (attempt {i + 1}).')
            subprocess.check_call([executable, "-m", "pip", "install", "--upgrade", package],
                                  creationflags=CREATE_NO_WINDOW)
            return True

        except subprocess.CalledProcessError:
            continue

    return False