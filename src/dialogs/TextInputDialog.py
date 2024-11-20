import wx


class TextInputSelectionDialog(wx.Dialog):
    def __init__(self, parent, title="Enter Text", size=(400, 300)):
        super().__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_RICH2
        )
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.SetSize(size)

    @property
    def text_value(self):
        return self.text_ctrl.GetValue()

    def set_text(self, text):
        self.text_ctrl.SetValue(text)

