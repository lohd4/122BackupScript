import wx
from dialogs import BackupTypeSelectionDialog
from GeneralFunctions import SwitchCases
from RunManager import RunManager
from src.dialogs.SingleFolderSelectionDialog import SingleFolderDialog


def handle_first_run(run_mgr):
    dialog = BackupTypeSelectionDialog.Dialog(None)
    result = dialog.ShowModal()
    selection = dialog.radio_options.GetStringSelection() if result == wx.ID_OK else None
    dialog.Destroy()

    if not selection:
        return False

    selected_files = SwitchCases.select_backup_option_sc(selection)
    if not selected_files:
        return False

    dialog = SingleFolderDialog(None, "Select where your backup will be saved")
    result = dialog.ShowModal()
    directory_path = dialog.selected_path if result == wx.ID_OK else None
    dialog.Destroy()

    if not directory_path:
        return False

    dialog = SingleFolderDialog(None, "Select where your backup log file will be saved")
    result = dialog.ShowModal()
    log_directory_path = dialog.selected_path if result == wx.ID_OK else None
    dialog.Destroy()

    if not log_directory_path:
        return False

    run_mgr.file_selection_config(selected_files)
    run_mgr.backup_type_config(selection)
    run_mgr.target_dir_config(directory_path)
    run_mgr.log_target_dir_config(log_directory_path)
    run_mgr.mark_as_run()

    return True


def handle_subsequent_run(run_mgr):
    backup_type = run_mgr.config["backup_type"]
    backup_list = run_mgr.config["files_to_backup"]
    target_dir = run_mgr.config["target_dir"]
    log_target_dir = run_mgr.config["log_target_dir"]

    SwitchCases.exec_backup(
        backup_type=backup_type,
        backup_list=backup_list,
        target_dir=target_dir,
        log_target_dir=log_target_dir
    )
    return True


def main():
    app = wx.App()

    try:
        run_mgr = RunManager()

        if run_mgr.is_first_run:
            success = handle_first_run(run_mgr)
        else:
            success = handle_subsequent_run(run_mgr)

        return success

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    finally:
        app.MainLoop()


if __name__ == '__main__':
    main()