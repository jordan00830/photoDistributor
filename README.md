## Photo Distributor

## Setup dev env

1. [Download wxPython Here](http://www.wxpython.org/download.php)
2. install py2app, enum

	```
	$ sudo pip install -U py2app
	$ sudo pip install enum
	```

## Test & Dev

  ```
  $ python photoDistributor.py
  ```

## Build mac executable file

  ```
  $ python setup.py py2app
  ```



## To Do
* [DONE] Show photos + control to next or prev photo
* [DONE] filter non img file 
* [DONE] tag photo + copy photo to target folder
* [DONE] FOLDER path : windows : \  , mac & linux : /
* [DONE] function : add & modify tag list (load tag list from file)
* [DONE] lick tagBtn to copy, click again to cancel
* [DONE] store tag status ( into memory)
* [DONE] layout version 1.0
* [DONE] add source img path infomation
* save photo distributor result (including source folder, target folder, tag list file ,tag status)
* Detect source dir file change

