cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
path = cwd & "\reinstallMerge.bat"
 
Set shell = CreateObject("Shell.Application")
shell.ShellExecute path,"","","runas",1
 
WScript.Quit