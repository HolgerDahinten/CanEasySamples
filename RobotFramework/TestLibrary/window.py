"""
filename: window.py
Description: Some Window Handling Function
"""
import win32gui

__version__ = '0.1'

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def Bring_Window_to_Front(windowname: str):
    """
    Brings the window with the given name to front of the screen
    """
    
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if windowname.lower() in i[1].lower():
            win32gui.ShowWindow(i[0],5)  # 5: Activates the window and displays it in its current size and position. 
            win32gui.ShowWindow(i[0],3)  # 3: Maximizes the specified window. 
            win32gui.SetForegroundWindow(i[0])
            break
