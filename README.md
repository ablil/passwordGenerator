# Random Password Generator 
Simple random password generator written in python3.<br/>
**Features**<br/>
* customize password length
* customize password complexity:
  * alpha: uppercase / lowercase characters.
  * numeric: numeric values
  * alphanumeric: characters and numbers.
  * hard: charachters + number + symbols
* store recent password in cache.
  
  [![asciicast](https://asciinema.org/a/316691.svg)](https://asciinema.org/a/316691)
  
## Installation
* Download
```
> git clone https://github.com/ablil/passwordgenerator.git
> cd passwordgenerator/
```

* create shorcut
```
> sudo cp app.py /usr/bin/password
> sudo chmod +x /usr/bin/password
```

## usage
```
usage: passwordGenerator.py [-h] [-l LENGTH]
                            [--alpha | --numeric | --alphanumeric | --hard]
                            [--recent RECENT | --empty-cache]

optional arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        Password length (default: 15)
  --alpha               use alphanumeric characters only (uppercase /
                        lowercase
  --numeric             use numeric values only
  --alphanumeric        user characters and numebrs. (This is the default
                        option)
  --hard                use characters, numbers and symbols (Recommanded)
  --recent RECENT       Get recent generated passwords
  --empty-cache         Empty Cache
```

