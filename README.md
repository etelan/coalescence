
# Coalescence

This is a python script for merging playset files for Stellaris.

## Installation

Just run the file, by double clicking.

Additionally, it supports command line arguments.

You have to set **both file paths** to skip file selection, and to use command arguments at all.

Additionally, take a **read into Overwrite but no skip confirmations**

### arg1 

base file path relative to script, or absolute

### arg2 

update file path relative to script, or absolute

### arg3

provide keyword 'skip' for skipping, or anything else for not skipping

### arg4

provide keyword 'overwrite' to overwrite duplicate playsets, or anything else for no

### Example

#### Just file paths

This will set your paths correctly, if the files are in the same folder as the script.

Skips file selection in the script.

```bash
& C:/Users/bob/AppData/Local/Programs/Python/Python39/python.exe g:/Coding/python/merger/coalescence.py base.sqlite base.sqlite
```

#### Skip confirmations
```bash
& C:/Users/bob/AppData/Local/Programs/Python/Python39/python.exe g:/Coding/python/merger/coalescence.py base.sqlite base.sqlite skip
```

#### Overwrite but no skip confirmations
```bash
& C:/Users/bob/AppData/Local/Programs/Python/Python39/python.exe g:/Coding/python/merger/coalescence.py base.sqlite base.sqlite noskip overwrite
```

#### All Arguments
```bash
& C:/Users/bob/AppData/Local/Programs/Python/Python39/python.exe g:/Coding/python/merger/coalescence.py base.sqlite base.sqlite skip overwrite
```


## Usage

Is self explanatory once it is running!

It will never modify the existing files, just generated a new file where the script is saved called `new.sqlite`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
