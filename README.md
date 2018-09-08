# cliffy

cliffy is a module which allows you to wrap an existing command line program in its own CLI with its own isolated history.

## Prompt

`[<return code>] (<wrapped-program>) > `

## Examples

### Help

```
>$ cliffy.py -h
usage: cliffy.py [-h] [-f HISTORYFILE] [-l HISTORYLIMIT] cli [cli ...]

positional arguments:
  cli                   The command around which the CLI should be wrapped.

optional arguments:
  -h, --help            show this help message and exit
  -f HISTORYFILE, --history-file HISTORYFILE
                        The history file to use.
  -l HISTORYLIMIT, --history-limit HISTORYLIMIT
                        The maximum number of history entries to retain in the
                        history file.
```

### Wrap an existing program

```
>$ cliffy.py git
[0] (git) > status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   cliffy/cliffy.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   .gitignore
        modified:   README.md
        modified:   cliffy/cliffy.py
        modified:   requirements.txt
        modified:   setup.py

[0] (git) > add --all
[0] (git) > status
On branch master
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        modified:   .gitignore
        modified:   README.md
        modified:   cliffy/cliffy.py
        modified:   requirements.txt
        modified:   setup.py

[0] (git) >^D
>$ 
```
