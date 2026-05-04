# inky-agents

## Setup

### Enable I2C and SPI

```bash
$ sudo raspi-config nonint do_i2c 0
$ sudo raspi-config nonint do_spi 0
```

Add this to `/boot/firmware/config.txt`:

```
dtoverlay=spi0-0cs
```

### Set the static IP

```bash
$ sudo nmtui edit "Wired connection 1"
```
