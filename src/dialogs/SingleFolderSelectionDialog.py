import wx


class SingleFolderDialog(wx.Dialog):
    def __init__(self, parent, title="Select Directory"):
        wx.Dialog.__init__(self, parent, title=title, size=(400, 500))

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.dir_picker = wx.DirPickerCtrl(
            self,
            message="Choose a directory",
            style=wx.DIRP_USE_TEXTCTRL | wx.DIRP_DIR_MUST_EXIST
        )
        main_sizer.Add(self.dir_picker, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, wx.ID_OK, "OK")
        cancel_button = wx.Button(self, wx.ID_CANCEL, "Cancel")
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(main_sizer)

    @property
    def selected_path(self):
        return self.dir_picker.GetPath()