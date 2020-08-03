# Binary files pattern finder

Finding patterns in binary files

#### Done

- work on window(finger-like) model
- Added support for repeating bytes
- add support for regex
- ditched window model
- made it run faster (currenty 8-16 sec per 8MB (dpends on dict size))
- commented and documented

## USAGE:

##### From command line:  

`
$/python patternFinder.py <filepath> <dictpath> minRepeats
`

optional args:

`--readsize READSIZE` how many bytes you want to read from the file?  
default is the whole file

`--chunksize CHUNKSIZE` how many bytes you want to parse at once?  
default is 4MB

`--time TIME` print how long the parsing took  
default is False

#### From a script:

`  
>>> import patternFinder  
>>> patternFinder.find_patterns(...) #same args as before, except pattern dict which should not be a path to a json file!
`
