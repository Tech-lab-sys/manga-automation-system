import logging
import os
import yaml
from dotenv import load_dotenv

def setup_logging(name: str = "manga_system") -> logging.Logger:
    """Setup centralized logging."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class ConfigManager:
    """Enterprise-standard configuration management."""
    def __init__(self, config_path: str = "config/config.yaml"):
        load_dotenv()
        self.config = self._load_yaml(config_path)

    def _load_yaml(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error(f"Failed to load config from {path}: {e}")
            return {}

    def get(self, key_path: str, default=None):
        keys = key_path.split('.')
        val = self.config
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def get_env(self, key: str, default=None):
        return os.getenv(key, default)
