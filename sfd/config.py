"""SFD config. Independent of SAF. Fails loudly."""
import yaml, os
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent.parent

class ConfigError(Exception): pass

@lru_cache(maxsize=1)
def load() -> dict:
    path = ROOT / "flowdesk.yaml"
    if not path.exists():
        raise ConfigError(f"Missing {path}")
    cfg = yaml.safe_load(path.read_text())
    _validate(cfg)
    return cfg

def _validate(cfg):
    s = cfg.get("settings", {})
    for key in ("instrument", "tick_size", "tick_value", "stop_ticks", "max_daily_loss"):
        if key not in s:
            raise ConfigError(f"settings.{key} required")
    if not os.getenv("POLYGON_API_KEY"):
        # Don't hard-crash; allow quant-dev without live data
        print("⚠️  POLYGON_API_KEY not set — running in data-dev mode")

def settings(cfg=None) -> dict:
    return (cfg or load())["settings"]