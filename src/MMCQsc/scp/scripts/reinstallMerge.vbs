cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
Set shell = CreateObject("Shell.Application")
command = "cd 'C:/Program Files/Python39';.\python -m pip install color-theme-analyse[merge]==1.108.2.dev0 --force-reinstall --trusted-host mirrors.tencent.com -i https://pypi.org/simple --extra-index-url https://mirrors.tencent.com/pypi/simple --timeout 30;'';'';'Press Enter to exit.';'';'回车键退出';[Console]::Readkey() | Out-Null ;Exit"
answer=MsgBox("当前进程绑定的 Pyhton 路径位于 C:/Program Files/Python39/python.exe" & vbCrLf & "请确认与项目的宿主 Python 一致。" & vbCrLf & "重装依赖包可能会导致不可控的影响，请慎重。",65,"是否重装所有额外依赖包？")
if  answer = vbOK then
    shell.ShellExecute "powershell",command,"","",1
End if
