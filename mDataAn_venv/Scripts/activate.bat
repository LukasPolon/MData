@echo off
set "VIRTUAL_ENV=C:\Users\LukaszP\Documents\Repos\lp_mgr_main\mDataAn_venv"

if defined _OLD_VIRTUAL_PROMPT (
    set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
) else (
    if not defined PROMPT (
        set "PROMPT=$P$G"
    )
	set "_OLD_VIRTUAL_PROMPT=%PROMPT%"	
)
set "PROMPT=(mDataAn_venv) %PROMPT%"

if not defined _OLD_VIRTUAL_PYTHONHOME (
    set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
)
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH (
    set "PATH=%_OLD_VIRTUAL_PATH%"
) else (
    set "_OLD_VIRTUAL_PATH=%PATH%"
)
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"

set TCL_LIBRARY=C:\Python27\tcl\tcl8.5
set TK_LIBRARY=C:\Python27\tcl\tk8.5

:END
