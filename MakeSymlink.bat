::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: mklink
::   Creates a symbolic link.
:: Syntax
::   mklink [[/d] | [/h] | [/j]] <Link> <Target>
:: Parameters
::   /d       - Creates a directory symbolic link. By default, mklink creates a
::              file symbolic link.
::   /h       - Create a hard link instead of a symbolic link.
::   /j       - Create a Directory Junction.
::   <Link>   - Specifies the name of the symbolic link that is being created.
::   <Target> - Specifies the path (relative or absolute) that the new symbolic
::              link refers to.
::   / ?      - Displays help at the command prompt.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set path=%~p0
set path=%path:~0,-1%
for %%A in ("%path%") do (set CurrentDirName=%%~nxA)

mklink /j ..\%AddOnDirName% %CurrentDirName%\%AddOnDirName%
