## Photo Distributor

## Setup dev env

* [Download & intall wxPython Here](http://www.wxpython.org/download.php)

 
#### MAC

```
$ sudo pip install -U py2app
$ sudo pip install enum
$ sudo pip install pillow
```
	
#### Windows	(Or use pip install)

[Download py2exe here](http://www.py2exe.org/)

[Download enum here](https://pypi.python.org/pypi/enum/) 

[Download & intall Pillow Here](https://pillow.readthedocs.org/installation.html)

## Test & Dev

```
$ python photoDistributor.py
```

## Build executable file
#### MAC
 
```
$ python setup.py py2app
```
#### WINDOWS

```
$ python setup_win.py py2exe
```


## To Do
* [DONE] Show photos + control to next or prev photo
* [DONE] filter non img file 
* [DONE] tag photo + copy photo to target folder
* [DONE] function : add & modify tag list (load tag list from file)
* [DONE] lick tagBtn to copy, click again to cancel
* [DONE] store tag status ( into memory)
* [DONE] layout version 1.0
* [DONE] add source img path infomation
* [DONE] support windows decoding
* [DONE] Keyboard arraow to change photo
* [DONE]Add author info
* [DONE]Final & first photo show msg
* Auto resize
* Rotate photo (BUG : black border)
* Alert if file exist and support rename file
* Automatically load tag btns when set up target folder
* add mask when loading photos
* RWD
* save photo distributor result (including source folder, target folder, tag list file ,tag status)
* Detect source dir file change

