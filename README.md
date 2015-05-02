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
* [Done]function : add & modify tag list (load tag list from file)
* [Done]lick tagBtn to copy, click again to cancel
* store tag status ( into file? memory?)
* copy files to target folder
* Detect source dir file change
* layout
