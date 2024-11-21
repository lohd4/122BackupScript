import json
import os


class RunManager:
    def __init__(self, config_file="run_config.json"):
        self.config_file = config_file
        self.has_run = self._check_if_has_run()
        self.config = self._load_config()

    def _check_if_has_run(self):
        print(os.path.exists(self.config_file))
        if os.path.exists(self.config_file):
            if self._check_has_run_file():
                return True
            else:
                return False
        else:
            return False

    def _check_has_run_file(self):
        f = open(self.config_file)
        data = json.load(f)
        f.close()
        return data["has_run"]

    def _load_config(self):
        if not self.has_run:
            config = {
                "has_run": False,
                "backup_type": None,
                "files_to_backup": None,
                "target_dir": None,
                "log_target_dir": None
                      }
            self._save_config(config)
            return config
        else:
            file = open(self.config_file)
            config = json.load(file)
            file.close()
            print (config)
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