# DeSnapper [![Build Status](https://travis-ci.com/Wanket/DeSnapper.svg?branch=master)](https://travis-ci.com/Wanket/DeSnapper)

DeSnapper is a GUI program for [snapper](https://github.com/openSUSE/snapper) writed on Python and Qt for Debian-based systems.
It have all snapper features plus useful diff but except rollback (don't work on Debian-based systems).

## Install program with dependencies

```
sudo dpkg -i diff-match-patch.deb
sudo dpkg -i sxsdiff.deb
sudo dpkg -i desnapper.deb
sudo apt install -f
```

Also you can install [DeSnapper-btrfs](https://github.com/Wanket/DeSnapper-btrfs) module for btrfs qgroups support
```
sudo dpkg -i desnapper-btrfs-amd64.deb # example for amd64
sudo apt install -f
```

## Screenshots

![](https://i.imgur.com/uoooGpe.png)
![](https://i.imgur.com/WVNqZ52.png)
