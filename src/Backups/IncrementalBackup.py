import os
import shutil
import hashlib
import json
import datetime
import logging
import errno
from pathlib import Path
from typing import List, Dict, Any


class IncrementalBackup:
    def __init__(self, backup_dir: str, manifest_path: str = "backup_manifest.json", log_dir: str = "backup_logs"):

        self.backup_dir = Path(backup_dir)
        self.manifest_path = Path(manifest_path)
        self.log_dir = Path(log_dir)

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._setup_logging()

        self.manifest = self._load_manifest()
        self.logger.info("Backup system initialized")

    def _setup_logging(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"backup_{timestamp}.log"

        self.logger = logging.getLogger('IncrementalBackup')
        self.logger.setLevel(logging.INFO)

        self.logger.handlers = []

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _load_manifest(self) -> Dict:

        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r') as f:
                    self.logger.info("Loading existing backup manifest")
                    return json.load(f)
            except json.JSONDecodeError:
                self.logger.warning("Corrupt manifest file found, creating new one")
                return self._create_new_manifest()
            except Exception as e:
                self.logger.error(f"Error loading manifest: {str(e)}")
                return self._create_new_manifest()
        return self._create_new_manifest()

    def _create_new_manifest(self) -> Dict:

        self.logger.info("Creating new backup manifest")
        return {
            'last_backup': None,
            'files': {}
        }

    def _save_manifest(self):
        try:
            with open(self.manifest_path, 'w') as f:
                json.dump(self.manifest, f, indent=4)
            self.logger.info("Backup manifest saved")
        except Exception as e:
            self.logger.error(f"Error saving manifest: {str(e)}")

    def _is_file_locked(self, file_path: Path) -> bool:

        try:
            with open(file_path, 'rb') as f:
                f.read(1)
                return False
        except (IOError, OSError) as e:
            if e.errno == errno.EACCES or e.errno == errno.EBUSY:
                return True
            raise

    def _safe_copy_file(self, src: Path, dest: Path) -> bool:

        try:
            if self._is_file_locked(src):
                self.logger.warning(f"File is locked/in use: {src}")
                return False

            dest.parent.mkdir(parents=True, exist_ok=True)

            with open(src, 'rb') as fsrc:
                with open(dest, 'wb') as fdst:
                    while True:
                        chunk = fsrc.read(65536)
                        if not chunk:
                            break
                        fdst.write(chunk)

            shutil.copystat(src, dest)
            return True

        except (IOError, OSError) as e:
            if e.errno == errno.EACCES:
                self.logger.warning(f"Access denied to file: {src}")
            elif e.errno == errno.EBUSY:
                self.logger.warning(f"File is busy: {src}")
            else:
                self.logger.error(f"Error copying file {src}: {str(e)}")
            return False

    def _calculate_file_hash(self, file_path: Path) -> str:

        try:
            if self._is_file_locked(file_path):
                return None

            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (IOError, OSError) as e:
            self.logger.warning(f"Could not calculate hash for {file_path}: {str(e)}")
            return None

    def _generate_backup_report(self, backup_time: str, stats: Dict[str, Any]):
        report_path = self.log_dir / f"backup_report_{backup_time}.txt"

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"Backup Report - {backup_time}\n")
                f.write("=" * 80 + "\n\n")

                f.write("Summary:\n")
                f.write(f"- Directories processed: {stats['directories_processed']}\n")
                f.write(f"- Total files processed: {stats['files_processed']}\n")
                f.write(f"- Files backed up: {stats['files_backed_up']}\n")
                f.write(f"- Files locked/in use: {stats['files_locked']}\n")
                f.write(f"- Files skipped: {len(stats['skipped_files'])}\n")
                f.write(f"- Files failed: {len(stats['failed_files'])}\n\n")

                f.write("Backed up files:\n")
                for file in stats['backed_up_files']:
                    f.write(f"+ {file}\n")
                f.write("\n")

                if stats['locked_files']:
                    f.write("Locked/In-use files:\n")
                    for file in stats['locked_files']:
                        f.write(f"* {file}\n")
                    f.write("\n")

                f.write("Skipped files (unchanged):\n")
                for file in stats['skipped_files']:
                    f.write(f"= {file}\n")
                f.write("\n")

                if stats['failed_files']:
                    f.write("Failed files:\n")
                    for file in stats['failed_files']:
                        f.write(f"! {file}\n")
                    f.write("\n")

                if stats['errors']:
                    f.write("Errors:\n")
                    for error in stats['errors']:
                        f.write(f"- {error}\n")

            self.logger.info(f"Backup report generated: {report_path}")
        except Exception as e:
            self.logger.error(f"Error generating backup report: {str(e)}")

    def backup_files(self, files_to_backup: List[str]) -> Dict[str, Any]:

        self.logger.info("Starting backup operation")

        backup_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        stats = {
            'files_processed': 0,
            'files_backed_up': 0,
            'files_locked': 0,
            'directories_processed': 0,
            'errors': [],
            'backed_up_files': [],
            'skipped_files': [],
            'locked_files': [],
            'failed_files': []
        }

        for source_path in files_to_backup:
            source_path = Path(source_path)
            try:
                if source_path.is_file():
                    self.logger.info(f"Processing single file: {source_path}")
                    files = [source_path]
                else:
                    self.logger.info(f"Processing directory: {source_path}")
                    stats['directories_processed'] += 1
                    files = [f for f in source_path.rglob("*") if f.is_file()]

                for file_path in files:
                    stats['files_processed'] += 1
                    try:
                        if self._is_file_locked(file_path):
                            stats['files_locked'] += 1
                            stats['locked_files'].append(str(file_path))
                            self.logger.warning(f"Skipping locked file: {file_path}")
                            continue

                        current_hash = self._calculate_file_hash(file_path)
                        if current_hash is None:
                            continue

                        file_key = str(file_path)

                        if (file_key not in self.manifest['files'] or
                                self.manifest['files'][file_key]['hash'] != current_hash):

                            backup_path = self.backup_dir / backup_time / file_path.relative_to(file_path.anchor)

                            if self._safe_copy_file(file_path, backup_path):
                                self.manifest['files'][file_key] = {
                                    'hash': current_hash,
                                    'last_backup': backup_time,
                                    'size': file_path.stat().st_size
                                }

                                stats['files_backed_up'] += 1
                                stats['backed_up_files'].append(str(file_path))
                                self.logger.info(f"Backed up file: {file_path}")
                            else:
                                stats['failed_files'].append(str(file_path))
                        else:
                            stats['skipped_files'].append(str(file_path))
                            self.logger.debug(f"Skipped unchanged file: {file_path}")

                    except Exception as e:
                        error_msg = f"Error processing {file_path}: {str(e)}"
                        stats['errors'].append(error_msg)
                        stats['failed_files'].append(str(file_path))
                        self.logger.error(error_msg)

            except Exception as e:
                error_msg = f"Error accessing {source_path}: {str(e)}"
                stats['errors'].append(error_msg)
                self.logger.error(error_msg)

        self.manifest['last_backup'] = backup_time
        self._save_manifest()

        self.logger.info(f"Backup completed at: {backup_time}")
        self.logger.info(f"Directories processed: {stats['directories_processed']}")
        self.logger.info(f"Files processed: {stats['files_processed']}")
        self.logger.info(f"Files backed up: {stats['files_backed_up']}")
        self.logger.info(f"Files locked/in use: {stats['files_locked']}")
        self.logger.info(f"Files skipped: {len(stats['skipped_files'])}")
        self.logger.info(f"Files failed: {len(stats['failed_files'])}")

        self._generate_backup_report(backup_time, stats)

        return stats

    def get_backup_history(self, file_path: str) -> Dict:
        file_key = str(Path(file_path))
        return self.manifest['files'].get(file_key, None)