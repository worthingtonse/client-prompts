# QMail Format For Phase I
The QMail is made up of three parts. Each part seperatd by the FS control character (ASCII 28 0x1C). FS means File Seperator

## Overall Structure
This is the structure of a QMail file for Phase I that is just for sending a text message
| Control Character | Name | Meaning | Description |
|---|---|---|---|
|n/a| [Meta Data File](meta-file.md)| This is seperat file|Concatinated to the next character |
|FS| File Seperator |ASCII 0x1C| The first FS begins the styles tables |
|---|---|---|---|
|---|---|---|---|
  [Meta Data File](meta-file.md)
FS
  Styles
FS
  STX (Start of Text ASCII Control Character. Decimal 28. Hex 0x1C.
The text starts here and keeps going until there are is no more writing.
```


  


