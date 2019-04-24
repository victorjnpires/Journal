Journal: One paragraph a day memory book
========================================

Write your thoughts and/or memories one paragraph a day and read the entries for the same day on previous years.


## Major releases

#### Version 2.0 (2019-04-20)
New entries are automatically sorted by year.

#### Version 1.0 (2019-01-25)
First release of the program.


## Requirements

* Python >= 3.6
* LaTeX


## Downloading

To clone with git:

    $ git clone https://github.com/victorjnpires/Journal.git


## Installing

Python is included on Debian and Debian-based distributions, such as Ubuntu and Linux Mint. All libraries used in this project are from the Python Standard Library that is distributed with Python.

For a basic installation of a TeX system:

    $ sudo apt install texlive-base

For a a complete TeX system:

    $ sudo apt install texlive-latex-base


## Running

    $ python Journal.py

The code will first look for the Journal files and folders inside the Documents folder in your home directory. If any of the files is missing it will prompt to create a new Journal folder with empty files. You must type `YES` to continue or the program will terminate.

### Making files and folders

```
>>>>> Journal: One paragraph a day memory book <<<<<

>>> WARNING!
>> This script will make the files and folders for the Journal.
>> It will delete all files from the folder '/home/victor/Documents/Journal'
>> Type 'YES' to continue
> YES
```

If you type anything other than `YES` the program will terminate with the following message:

```
>>> ERROR: No changes were made!

>>> ERROR: Journal files and folders not found!
```

If you type `YES` the program will ask for and author’s name and journal title.

```
>>> New journal
>> Author
> Victor Jose Novaes Pires
>> Title (Victor's Journal)
> Victor's Journal

>>> Making files and folders...
```

### Adding an entry

After making the files and folders, and on any execution of the program henceforth, it will display a date and ask for an entry.

```
>>> Friday, January 25, 2019
>> Today was a good day, I have finished my Journal program and I'm ready to upload it to GitHub.   :D
```

Once you're done with your daily paragraph it will ask you if you want to save. If you don’t confirm no changes will be made to the Journal.

```
>> Save? [Y/n]: NO

>>> No changes were saved!
```

To save just press `Enter` to continue with the default option `YES`.

```
>> Save? [Y/n]: YES
```

Once you confirm the program will compile the Journal with the new entry and it will be in `~/Documents/Journal/Journal.pdf`.

```
>>> Building journal...
(...)
```

Once compiled the program will try opening `Journal.pdf` with your default PDF viewer. If there isn't a default PDF viewer the following message will appear:

```
>>> Couldn't display Journal.pdf
```

Regardless of the display of `Journal.pdf` after compiled the file should be in your folder and the following message will confirm that the program has run as expected:

```
>>> Program finished successfully!
```

### Adding an entry for other dates

To add an entry for a date other than today just type the desired date in the format Year-Month-Day (`YYYY-MM-DD`). The program will prompt you again for an entry on the new date and will proceed like the section `Adding an entry` above.

```
>>> Friday, January 25, 2019
>> 2019-01-24

>>> Thursday, January 24, 2019
>> This was a log day and I am almost done with my new project!   :)
```

Since version 2.0 new entries are automatically sorted by year. Also, when entering a date, the zero in front of a day or month is now optional.

```
>>> Tuesday, April 23, 2019
>> 2019-4-20

>>> Saturday, April 20, 2019
>> Making older entries was never so easy now that they will be sorted by year.   ^.^
```


## Example

Example.pdf is a file that was filled with Lorem Ipsum, pseudo-Latin text, to illustrate how the journal would look like with text after five years of entries.


## Author

Victor Jose Novaes Pires

[https://victorjnpires.github.io/](https://victorjnpires.github.io/)
