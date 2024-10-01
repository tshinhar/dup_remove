# dup_remove
python code for removing duplicate files

to use, simpley run the python script and pass it the root directory you want to remove duplicates from.
for example:
`python remove_duplicates.py {path_to_dir}`
the script will go over all files in the directory and any sub-directories under it and will list all the duplicate files before removing them.
by default, the script will ask before removing each of the files, if you want to allow the script to delete all duplicate files without asking, run:
`python remove_duplicates.py %cd% -y`

if you want to be able to access the script from any directory, you would need to add it to PATH
