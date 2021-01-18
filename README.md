# Make Noise

## What is **make_noise**?
The **make_noise** application strives to live up to its name by
making noise.  It does this with
[`sox`](http://sox.sourceforge.net/Main/HomePage).  Although it tries,
it may not succeed.  This is because **make_noise** is a hastily made
wrapper around [the `noise.sh`
gist](https://gist.github.com/xguse/6259275).  It runs on Windows and
Linux.

## Design goals
The objective is simple: create a taskbar application to toggle noise
as quickly as possible.  This was achieved by constructing a sox call
string (the one given in the gist, actually), starting a subprocess,
and passing the sox call string.

This is the string:

```
sox --no-show-progress -c 2 --null synth 3600 brownnoise band -n 1500 499 tremolo 0.05 43 reverb 19 bass -11  treble -1 vol 14dB  fade q .01 repeat 9999
```

To stop the noise, the subprocess is ruthlessly killed.

## Quick start
Try one of the binaries.  If it works, great!  If not, try running or
building [from source](#From-source).

The call and kill are combined in a beautiful default-style taskbar
button.  When the button is green, there should be no noise.  Double
clicking the green button makes noise:

![a green button](extras/green-button.png "Green Button")

When there is noise, the button is red.  Double clicking the red
button stops the noise:

![a red button](extras/red-button.png "Red Button")

## From source
With all respect, please note that

> For the developers' and authors' protection, the GPL clearly
> explains that there is no warranty for this free software.

and recall that a "warranty" is

> written guarantee of the integrity of a product and of the maker's
> responsibility for the repair or replacement of defective parts

This software is licensed under the GPL.

Requirements

- Python 3.7.3 (could probably use 3.6)
- PySide2 (built on Linux with 5.15.1, Windows 5.15.2)
- SoX v14.4.2 (if I didn't bundle it correctly)

Binaries were created with PyInstaller 4.2 using the command:

```
pyinstaller make_noise.spec --onefile
```
