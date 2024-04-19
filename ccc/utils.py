import re

from pathlib import Path

from loguru import logger as log

INPUT_FILE_GLOB = "*.in"


def infer_current_level(path: Path | str):
    path = Path(path)
    files = list(path.glob(INPUT_FILE_GLOB))
    if not files:
        log.warning(f"no input files in {path.resolve()}")
        return None

    levels = set()
    for file in files:
        if match := re.search(r"level(\d+)", file.name):
            levels.add(int(match.group(1)))

    current_level = max(levels)
    log.info(f"inferred current level: {current_level}")
    return current_level


def infer_quests_for_level(path: Path | str, level: int):
    if level is None:
        log.warning("cannot infer quests without a level")
        return []
    
    path = Path(path)
    files = list(path.glob(INPUT_FILE_GLOB))
    if not files:
        log.warning(f"no input files for level {level} in {path.resolve()}")
        return []

    quests = set()
    for file in files:
        if match := re.search(rf"level{level}_(\d+)", file.name):
            quests.add(int(match.group(1)))

    quests = list(sorted(quests))
    log.info(f"inferred quests for level {level}: {quests}")
    return quests