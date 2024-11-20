import wx


class FileSelectionDialog(wx.Dialog):
    def __init__(self, parent, title="Select file to back up", label="Choose a file", size=(400, 300)):
        super().__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.file_picker = wx.FilePickerCtrl(
            self,
            message=label,
            wildcard="Python files (*.py)|*.py|All files (*.*)|*.*",
            style=wx.FLP_USE_TEXTCTRL | wx.FLP_OPEN
        )
        sizer.Add(self.file_picker, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.SetSize(size)

    @property
    def selected_path(self):
        return self.file_picker.GetPath()
