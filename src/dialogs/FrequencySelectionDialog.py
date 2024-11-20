import wx


class FrequencySelectionDialog(wx.Dialog):
    def __init__(self, parent, title="Select Frequency", size=(300, 200)):
        super().__init__(parent, title=title)

        self.choices = {
            "DAILY": 2,
            "WEEKLY": 3,
            "MONTHLY": 4,
            "ONCE": 1
        }

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.radio_box = wx.RadioBox(
            self,
            label="Select Frequency",
            choices=list(self.choices.keys()),
            majorDimension=1,
            style=wx.RA_SPECIFY_COLS
        )
        sizer.Add(self.radio_box, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.SetSize(size)

    @property
    def selected_value(self):
        return list(self.choices.keys())[self.radio_box.GetSelection()]

    @property
    def selected_id(self):
        return self.choices[self.selected_value]

    def set_selection(self, value):
        if value in self.choices:
            self.radio_box.SetSelection(list(self.choices.keys()).index(value))


app = wx.App()

app.OnExit()
