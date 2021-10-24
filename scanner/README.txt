# Scanner
Uses an (_Adafruit 128x64 OLED Bonnet for the Respberry Pi_)[https://www.adafruit.com/product/3531] as a display and input device.

## Requirements

For scanning interfacing with the scanner, we use `scanimage`, which can be found [here](https://linux.die.net/man/1/scanimage).

```
sudo apt-get install -y python3-pil python3-pip imagemagick
sudo pip3 install -r scanner/requirements.txt
```


## Usage

You must run with `sudo` as we have to access memory locations on the pi to interface with the adafruit bonnet.

```
sudo python3 -m scanner
```
