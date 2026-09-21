import ctypes
from ctypes import wintypes

# Windows Restart Manager API to find locking process
RmGetList = ctypes.windll.rstrtmgr.RmGetList
RmStartSession = ctypes.windll.rstrtmgr.RmStartSession
RmRegisterResources = ctypes.windll.rstrtmgr.RmRegisterResources
RmEndSession = ctypes.windll.rstrtmgr.RmEndSession

CCH_RM_MAX_APP_NAME = 255
CCH_RM_MAX_SVC_NAME = 63

class RM_UNIQUE_PROCESS(ctypes.Structure):
    _fields_ = [
        ("dwProcessId", wintypes.DWORD),
        ("ProcessStartTime", wintypes.FILETIME)
    ]

class RM_PROCESS_INFO(ctypes.Structure):
    _fields_ = [
        ("Process", RM_UNIQUE_PROCESS),
        ("strAppName", wintypes.WCHAR * (CCH_RM_MAX_APP_NAME + 1)),
        ("strServiceShortName", wintypes.WCHAR * (CCH_RM_MAX_SVC_NAME + 1)),
        ("ApplicationType", wintypes.DWORD),
        ("AppStatus", wintypes.ULONG),
        ("TSSessionId", wintypes.DWORD),
        ("bRestartable", wintypes.BOOL)
    ]

def find_lockers(filepath):
    session_handle = wintypes.DWORD()
    session_key = (wintypes.WCHAR * 33)()
    res = RmStartSession(ctypes.byref(session_handle), 0, session_key)
    if res != 0:
        print(f"RmStartSession failed with error: {res}")
        return

    try:
        files = (wintypes.LPCWSTR * 1)(filepath)
        res = RmRegisterResources(session_handle, 1, files, 0, None, 0, None)
        if res != 0:
            print(f"RmRegisterResources failed with error: {res}")
            return

        n_proc_info_needed = wintypes.UINT(0)
        n_proc_info = wintypes.UINT(0)
        reboot_reasons = wintypes.DWORD()

        res = RmGetList(session_handle, ctypes.byref(n_proc_info_needed), ctypes.byref(n_proc_info), None, ctypes.byref(reboot_reasons))
        if res != 234 and res != 0: # 234 is ERROR_MORE_DATA
            print(f"RmGetList (1) failed with error: {res}")
            return

        if n_proc_info_needed.value == 0:
            print("No locking processes reported by Restart Manager.")
            return

        n_proc_info.value = n_proc_info_needed.value
        proc_infos = (RM_PROCESS_INFO * n_proc_info.value)()
        res = RmGetList(session_handle, ctypes.byref(n_proc_info_needed), ctypes.byref(n_proc_info), proc_infos, ctypes.byref(reboot_reasons))
        if res != 0:
            print(f"RmGetList (2) failed with error: {res}")
            return

        print(f"Found {n_proc_info.value} process(es) locking '{filepath}':")
        for i in range(n_proc_info.value):
            p = proc_infos[i]
            print(f"  PID: {p.Process.dwProcessId}, AppName: {p.strAppName}")

    finally:
        RmEndSession(session_handle)

if __name__ == "__main__":
    find_lockers(r"C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx")
