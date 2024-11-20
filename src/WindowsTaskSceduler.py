import win32com.client
from datetime import datetime
import sys
import os
import win32security
import win32api


class WindowsTaskScheduler:
    TRIGGER_TYPES = {
        "DAILY": 2,
        "WEEKLY": 3,
        "MONTHLY": 4,
        "ONCE": 1
    }

    def __init__(self):
        self.scheduler = win32com.client.Dispatch('Schedule.Service')
        self.scheduler.Connect()
        self.root_folder = self.scheduler.GetFolder('\\')

    def create_task(self, name, program_path, schedule_time, frequency="DAILY"):
        try:
            domain = win32api.GetDomainName()
            username = win32api.GetUserName()
            user = f"{domain}\\{username}" if domain else username

            if program_path.endswith('.py'):
                python_exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
                command = f'"{python_exe}" "{os.path.abspath(program_path)}"'
            else:
                command = f'"{os.path.abspath(program_path)}"'

            task_def = self.scheduler.NewTask(0)

            settings = task_def.Settings
            settings.Enabled = True
            settings.StartWhenAvailable = True
            settings.Hidden = False
            settings.RunOnlyIfNetworkAvailable = False
            settings.DisallowStartIfOnBatteries = False
            settings.StopIfGoingOnBatteries = False
            settings.MultipleInstances = 3
            settings.ExecutionTimeLimit = "PT72H"

            principal = task_def.Principal
            principal.UserId = user
            principal.LogonType = 3
            principal.RunLevel = 1

            trigger = task_def.Triggers.Create(self.TRIGGER_TYPES[frequency])
            trigger.Enabled = True
            trigger.StartBoundary = schedule_time.strftime("%Y-%m-%dT%H:%M:00")

            if frequency == "DAILY":
                trigger.DaysInterval = 1
            elif frequency == "WEEKLY":
                trigger.DaysOfWeek = 0x1
                trigger.WeeksInterval = 1
            elif frequency == "MONTHLY":
                trigger.DaysOfMonth = 0x1
                trigger.MonthsOfYear = 0xFFF
            elif frequency == "ONCE":
                pass

            action = task_def.Actions.Create(0)
            if program_path.endswith('.py'):
                action.Path = python_exe
                action.Arguments = f'"{os.path.abspath(program_path)}"'
            else:
                action.Path = os.path.abspath(program_path)

            print(f"Creating task with these parameters:")
            print(f"Name: {name}")
            print(f"Command: {command}")
            print(f"User: {user}")
            print(f"Start time: {trigger.StartBoundary}")
            print(f"Frequency: {frequency}")

            self.root_folder.RegisterTaskDefinition(
                name,
                task_def,
                6,
                user,
                None,
                3
            )

            return True

        except Exception as e:
            print(f"Detailed error info:")
            print(f"Task name: {name}")
            print(f"Program path: {program_path}")
            print(f"Schedule time: {schedule_time}")
            print(f"Frequency: {frequency}")
            raise Exception(f"Failed to create task: {str(e)}")

