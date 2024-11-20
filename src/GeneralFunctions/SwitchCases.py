from datetime import datetime
import wx
import sys

from src.Backups.IncrementalBackup import IncrementalBackup
from src.WindowsTaskSceduler import WindowsTaskScheduler
from src.dialogs.FileSelectionDialog import FileSelectionDialog
from src.dialogs.DateTimeSelectionDialog import DateTimeSelectionDialog
from src.dialogs.FolderSelectionDialog import FolderSelectionDialog
from src.dialogs.FrequencySelectionDialog import FrequencySelectionDialog
from src.dialogs.TextInputDialog import TextInputSelectionDialog

def select_backup_option_sc(value):
    match value:
        case "Incremental":
            try:
                file_selections = None
                task_name = None
                selected_datetime = None
                file_selection = None
                frequency = None

                folder_dialog = FolderSelectionDialog(None)
                if folder_dialog.ShowModal() == wx.ID_OK:
                    file_selections = folder_dialog.selected_paths
                folder_dialog.Destroy()
                if not file_selections:
                    return None

                name_dialog = TextInputSelectionDialog(None, title="Select name for task")
                if name_dialog.ShowModal() == wx.ID_OK:
                    task_name = name_dialog.text_value
                name_dialog.Destroy()
                if not task_name:
                    return None

                datetime_dialog = DateTimeSelectionDialog(None, title="Select start date and start time for task")
                if datetime_dialog.ShowModal() == wx.ID_OK:
                    selected_datetime = datetime_dialog.datetime_value
                datetime_dialog.Destroy()
                if not selected_datetime:
                    return None

                file_dialog = FileSelectionDialog(None, title="Select file to run in task",
                    label="Please choose the executable file or this program wont work it may be called MainScript.py or a different name specified by the user")
                if file_dialog.ShowModal() == wx.ID_OK:
                    file_selection = file_dialog.selected_path
                file_dialog.Destroy()
                if not file_selection:
                    return None

                freq_dialog = FrequencySelectionDialog(None)
                if freq_dialog.ShowModal() == wx.ID_OK:
                    frequency = freq_dialog.selected_value
                freq_dialog.Destroy()
                if not frequency:
                    return None

                scheduler = WindowsTaskScheduler()
                scheduler.create_task(
                    name=task_name,
                    program_path=file_selection,
                    schedule_time=selected_datetime,
                    frequency=frequency
                )

                return file_selections

            except Exception as e:
                print(f"Error in backup option selection: {str(e)}")
                return None

        case "Full":
            return "NOT IMPLEMENTED YET"

def exec_backup(backup_type, backup_list, target_dir, log_target_dir):
    match backup_type:
        case "Incremental":
            backup = IncrementalBackup(backup_dir=target_dir, log_dir=log_target_dir)
            backup.backup_files(backup_list)
        case "Full":
            return "NOT IMPLEMENTED YET"