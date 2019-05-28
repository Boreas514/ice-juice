
import winreg
import subprocess

def check_uac():
    uac_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System')
    val=_winreg.QueryValueEx(uac_key, "EnableLUA")
    if val[0] == 1:
        return "\nUAC is Enabled"
    else:
        return "\nUAC is Disabled"

print(check_uac())