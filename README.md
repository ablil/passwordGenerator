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
USAGE:
core commands:
    generate:   generate passwords
    list:       list recent generated password
    clear:      clear store passwords

command aliases:
    generate:   g, gen, generate
    list:       l, ls, list
    clear:      c, clear, wipe
```

