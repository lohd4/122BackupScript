import wx


class FolderSelectionDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Select Folders")

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.dir_ctrl = wx.GenericDirCtrl(
            self,
            style=wx.DIRCTRL_MULTIPLE | wx.DIRCTRL_DIR_ONLY
        )
        sizer.Add(self.dir_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.SetSize((400, 500))

    @property
    def selected_paths(self):
        tree = self.dir_ctrl.GetTreeCtrl()
        return [
            self.dir_ctrl.GetPath(item)
            for item in tree.GetSelections()
        ]
