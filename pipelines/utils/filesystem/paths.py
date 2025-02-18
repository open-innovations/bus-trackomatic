from pathlib import Path

_ROOT = (Path(__file__).parent / '../../..').resolve()

MAPS = _ROOT / 'docs/maps'

DOWNLOADS = _ROOT / 'downloads'

ARXIV = DOWNLOADS / 'gtfs-rt/archive'

MAPS.mkdir(exist_ok=True, parents=True)

DOWNLOADS.mkdir(exist_ok=True, parents=True)

ARXIV.mkdir(exist_ok=True, parents=True)

# print(DOWNLOADS, MAPS)