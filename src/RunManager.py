import json
import os


class RunManager:
    def __init__(self, config_file="run_config.json"):
        self.config_file = config_file
        self.is_first_run = not os.path.exists(config_file)
        self.config = self._load_config()

    def _load_config(self):
        if self.is_first_run:
            config = {
                "has_run": False,
                "backup_type": None,
                "files_to_backup": None,
                "target_dir": None,
                "log_target_dir": None
                      }
            self._save_config(config)
            return config
        with open(self.config_file, 'r') as f:
            return json.load(f)

    def _save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def mark_as_run(self):
        self.config["has_run"] = True
        self._save_config(self.config)

    def file_selection_config(self, files_to_backup):
        self.config["files_to_backup"] = files_to_backup
        self._save_config(self.config)

    def backup_type_config(self, backup_type):
        self.config["backup_type"] = backup_type
        self._save_config(self.config)

    def target_dir_config(self, target_dir):
        self.config["target_dir"] = target_dir
        self._save_config(self.config)

    def log_target_dir_config(self, log_target_dir):
        self.config["log_target_dir"] = log_target_dir
        self._save_config(self.config)