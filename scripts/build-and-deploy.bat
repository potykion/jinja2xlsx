Rem %1 = minor | major | patch
call scripts\bump-version.bat %1
call scripts\deploy-pypi.bat