rmdir ..\dist /s /q
pyinstaller ../solitaire.py -n solitaire-py
rmdir build /s /q
del solitaire-py.spec
robocopy /s ../resources dist/solitaire-py/resources
copy dist\solitaire-py\resources\images\Ace-of-Clubs.ico .
ResourceHacker.exe -script changeIcon.txt
del Ace-of-Clubs.ico 
del dist\solitaire-py\solitaire-py.exe
rename dist\solitaire-py solitaire
move dist ..\dist