import wx

class Dialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Choose a Backup option", size=(300, 200))

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Please select your wanted Backup option:")
        vbox.Add(title, 0, wx.ALL | wx.CENTER, 5)

        self.radio_options = wx.RadioBox(
            panel,
            label="Backup options",
            choices=["Incremental", "Full"],
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS
        )
        vbox.Add(self.radio_options, 0, wx.ALL | wx.EXPAND, 5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, wx.ID_OK, "OK")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, "Cancel")

        button_sizer.Add(ok_button, 0, wx.ALL, 0)
        button_sizer.Add(cancel_button, 0, wx.ALL, 0)
        vbox.Add(button_sizer, 0, wx.ALL | wx.CENTER, 0)

        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

        panel.SetSizer(vbox)

        self.Center()

    def on_ok(self, event):
        event.Skip()
