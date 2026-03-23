# Fily
<<<<<<< Updated upstream
a cli tool for file managment.
=======
a cli tool for file management.
>>>>>>> Stashed changes

the tool currently supports organizing all files in a given directory as well as removing all duplicate files under the given root directory.
to use, simply run the python code and pass it the root directory you want to perform the operation on, as well as the wanted option.
by default, removing duplicates will be used, for example:
`python main {path_to_dir}`
the tool will go over all files in the directory and any sub-directories under it and will list all the duplicate files before removing them.
by default, the script will ask before removing each of the files, if you want to allow the script to delete all duplicate files without asking, run:
`python main -y {path_to_dir}`

to organize files, you would need to select one of the available options:
`python main {path_to_dir} -o`
this option will organize all files to directories based on their file extensions.

`python main {path_to_dir} -o -s`
this option will organize all files to directories based on some common logic, for example, all images will be moved to an "images" 
directory, videos to "movies" directory, etc.

dry-run mode:
`python main {path_to_dir} -d`
or
`python main {path_to_dir} --dry-run`
this option previews all actions without executing them. useful for seeing what would be deleted or moved before committing changes.
works with both remove duplicates and organize operations.

additional options:
- `-n THREADS` : set number of threads for parallel organization (default: 1)
- `.git`, `__pycache__`, `node_modules`, and `.DS_Store` are excluded by default

if you want to be able to access the tool from any directory, you would need to add it to PATH
