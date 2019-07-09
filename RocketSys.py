import wx

import matplotlib
matplotlib.interactive(True)
matplotlib.use('WxAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

import numpy as np


class MainWindow(wx.Frame):
    """
    Top Level Window Class
    """
    def __init__(self):
        super().__init__(None, wx.ID_ANY, 'Rocket System Information App')
        self.Maximize(True)
        self.SetBackgroundColour('BLACK')

        # Setting Status Bar
        self.CreateStatusBar()
        self.SetStatusText('Function Correctly.')

        # Setting Menu Bar
        self.SetMenuBar(AppMenu())

        # Making Main Graphic
        root_panel = wx.Panel(self, wx.ID_ANY)

        chart_panel = ChartPanel(root_panel)
        chart_panel.SetBackgroundColour('GRAY')
        system_panel = SystemPanel(root_panel)
        system_panel.SetBackgroundColour('GRAY')

        root_layout = wx.GridSizer(cols=2, gap=(20,0))
        root_layout.Add(chart_panel, flag=wx.EXPAND | wx.ALL,border=20)
        root_layout.Add(system_panel, flag=wx.EXPAND | wx.ALL,border=20)
        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)

        self.Bind(wx.EVT_CLOSE, self.onExit)

    def onExit(self, event):
        dig = wx.MessageDialog(self,
        "Do you really want to close this application?",
        "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dig.ShowModal()
        dig.Destroy()
        if result == wx.ID_OK:
            wx.Exit()

class ChartPanel(wx.Panel):
    """
    Quick Plot Graph Class
    """
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        self.lastplot_1 = None
        self.lastplot_2 = None
        self.lastplot_3 = None

        self.figure_1 = Figure()
        self.axes_1 = self.figure_1.add_subplot(111)
        self.canvas_1 = FigureCanvasWxAgg(self, -1, self.figure_1)

        self.figure_2 = Figure()
        self.axes_2 = self.figure_2.add_subplot(111)
        self.canvas_2 = FigureCanvasWxAgg(self, -1, self.figure_2)

        self.figure_3 = Figure()
        self.axes_3 = self.figure_3.add_subplot(111)
        self.canvas_3 = FigureCanvasWxAgg(self, -1, self.figure_3)

        self.graphGenerator()

        layout = wx.GridSizer(3, 1, gap=(10, 10))
        layout.Add(self.canvas_1, flag=wx.EXPAND)
        layout.Add(self.canvas_2, flag=wx.EXPAND)
        layout.Add(self.canvas_3, flag=wx.EXPAND)
        self.SetSizer(layout)

        self.timer_reload = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.graphReloader, self.timer_reload)
        self.timer_reload.Start(150)

    def graphGenerator(self):
        self.t = np.arange(0, 2 * np.pi, 0.1)

        self.x = np.sin(self.t)
        self.axes_1.plot(self.t, self.x)
        self.axes_1.set_xlabel('time[s]')
        self.axes_1.set_ylabel('pressure[MPa]')

        self.y = np.cos(self.t)
        self.axes_2.plot(self.t, self.y)
        self.axes_2.set_xlabel('time[s]')
        self.axes_2.set_ylabel('temperature[K]')

        self.z = self.t
        self.axes_3.plot(self.t, self.z)
        self.axes_3.set_xlabel('time[s]')
        self.axes_3.set_ylabel('acceleration[m/s^2]')

    def graphReloader(self, event):
        self.axes_1.cla()
        self.axes_2.cla()
        self.axes_3.cla()

        self.t = self.t + 0.1

        self.x = np.sin(self.t) * np.sqrt(self.t)
        self.axes_1.plot(self.t, self.x)
        self.axes_1.set_xlabel('time[s]')
        self.axes_1.set_ylabel('pressure[MPa]')
        self.canvas_1.draw()

        self.y = 200. + 100. * np.sin(self.t) * np.cos(self.t)
        self.axes_2.plot(self.t, self.y)
        self.axes_2.set_xlabel('time[s]')
        self.axes_2.set_ylabel('temperature[K]')
        self.canvas_2.draw()

        self.z = self.t * np.sin(self.t)
        self.axes_3.plot(self.t, self.z)
        self.axes_3.set_xlabel('time[s]')
        self.axes_3.set_ylabel('acceleration[m/s^2]')
        self.canvas_3.draw()


class SystemPanel(wx.Panel):
    """
    System Condition Class
    """
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        self.button_1 = wx.Button(self, wx.ID_ANY, 'System1')
        self.button_1.Bind(wx.EVT_BUTTON, self.onToggle)

        self.button_2 = wx.Button(self, wx.ID_ANY, 'System2')

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.button_1, flag=wx.ALIGN_CENTER | wx.SHAPED)
        layout.Add(self.button_2, flag=wx.ALIGN_CENTER | wx.SHAPED)
        self.SetSizer(layout)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onToggle, self.timer)
        self.timer.Start(5000)

    def onToggle(self, event):
        btnLabel = self.button_1.GetLabel()
        if btnLabel == 'System1':
            self.button_1.SetLabel('System1 Error')
            self.button_1.SetForegroundColour('RED')
        else:
            self.button_1.SetLabel('System1')
            self.button_1.SetForegroundColour('BLACK')

class AppMenu(wx.MenuBar):
    """
    Application Menu Bar Class
    """
    def __init__(self):
        super().__init__()

        menu_file = wx.Menu()
        menu_file.Append(1, 'Open')
        menu_file.Append(2, 'Save')
        menu_file.Append(3, 'Exit')
        menu_edit = wx.Menu()
        menu_edit.Append(4, 'Reload')
        menu_edit.Append(5, 'Delete')

        self.Append(menu_file, 'File')
        self.Append(menu_edit, 'Edit')

        self.Bind(wx.EVT_MENU, self.onExit)

    def onExit(self, event):
        event_id = event.GetId()
        if event_id == 3:
            dig = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            result = dig.ShowModal()
            dig.Destroy()
            if result == wx.ID_OK:
                wx.Exit()

if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()

    app.MainLoop()
