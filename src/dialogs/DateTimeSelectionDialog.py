import wx
import wx.adv
from datetime import datetime


class DateTimeSelectionDialog(wx.Dialog):
    def __init__(self, parent, title="Select Date and Time", size=(300, 200)):
        super().__init__(parent, title=title)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.date_picker = wx.adv.DatePickerCtrl(
            self,
            style=wx.adv.DP_DEFAULT | wx.adv.DP_SHOWCENTURY
        )
        sizer.Add(self.date_picker, 0, wx.EXPAND | wx.ALL, 5)

        self.time_picker = wx.adv.TimePickerCtrl(
            self,
            style=wx.adv.TP_DEFAULT
        )
        sizer.Add(self.time_picker, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_RIGHT)

        self.SetSizer(sizer)
        self.SetSize(size)

    @property
    def datetime_value(self):
        date = self.date_picker.GetValue()
        time = self.time_picker.GetValue()
        return datetime(
            date.year, date.month, date.day,
            time.hour, time.minute, time.second
        )

    def set_datetime(self, dt):
        self.date_picker.SetValue(dt)
        self.time_picker.SetValue(dt)


