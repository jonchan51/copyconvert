# CopyConvert

Copy, and optionally convert, files between directories.

File conversions use CloudConvert, and requires a CloudConvert api key, which
can be optained at https://cloudconvert.com/dashboard/api/v2/keys. Do note that
the free tier only allows for 25 minutes of conversion time a day. Any
further conversions will cause an error.

## Motivation

This tool has a very specific usecase: to copy, and convert files downloaded
via [fluminurs](https://github.com/indocomsoft/fluminurs) into my DropBox folder,
as I realise I waste a lot of time manually copying files over. 

## Setup
Requires pipenv and python 3.6
```
pipenv install
```
If you are converting files as well,
```
cp .env.example .env
```
Then add your CloudConvert api key into the `.env` file.

## Examples
### Copying files
Currently, it expects absolute filepaths to be passed as inputs. Every
filepath should be located within the source folder. The copied file will have the 
same relative filename in the destination folder. For example, suppose we run with
```
pipenv run python copyconvert/main.py -s /home/user/Downloads/ -d /home/user/Documents/
```
and in the REPL, we input `/home/user/Downloads/abc/def.doc`. Then it will be
moved to `/home/user/Documents/abc/def.doc` accordingly, creating the directory
'abc' if it does not exist within the 'Documents' folder. 

If the file already exists in the destination directory, CopyConvert skips the file.

Recommended to pass in input via `grep` or file redirection. For file redirection,
each filepath should be on a separate line.

### Converting files
```
pipenv run python copyconvert/main.py -s /home/user/Downloads/ -d /home/user/Documents/ -c doc pdf -c docx pdf
```
Files which have the extension doc will be converted using CloudConvert, then
copied over to the destination directory. Other files will just be copied without
conversion.

### Skipping files
```
pipenv run python copyconvert/main.py -s /home/user/Downloads/ -d /home/user/Documents/ -c doc pdf -c docx pdf --skip /skipme/
```
Does the same as the previous example, but skips a file if the filepath contains '/skipme/'.
This string can be replaced with anything, CopyConvert just checks whether the filepath 
contains the string.

## Potential Future Features
- Multithreading
- Scan source folder instead of reading from input (Copy everything that is not in destination folder)
- Convert without copying
- Regex instead of a plain string
- Copy if regex matches
- Rename folders
