import os
import yaml
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

class ConfigLoader:
    """Loads configuration from YAML and environment variables."""

    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        load_dotenv()

    def _load_config(self) -> dict:
        """Loads the YAML configuration file."""
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"Error loading config file: {e}")
            return {}

    def get(self, key, default=None):
        """Gets a configuration value."""
        return self.config.get(key, default)

def setup_logger(name: str, log_file: str = "app.log", level: int = logging.INFO) -> logging.Logger:
    """Sets up a professional logger with file and console handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console Handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File Handler (Rotating)
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)
        fh = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Global instances for convenience
config = ConfigLoader()
logger = setup_logger("manga_automation", log_file="output/logs/app.log")
