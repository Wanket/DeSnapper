#!/bin/bash

cd "${0%/*}"

(
  mkdir -p desnapper/usr/lib/python3/dist-packages/DeSnapper

  cp -r ../qt_snapper desnapper/usr/lib/python3/dist-packages/DeSnapper
  cp -r ../snapper desnapper/usr/lib/python3/dist-packages/DeSnapper
  cp -r ../utils desnapper/usr/lib/python3/dist-packages/DeSnapper
  cp -r ../widgets desnapper/usr/lib/python3/dist-packages/DeSnapper
  cp -r ../main.py desnapper/usr/lib/python3/dist-packages/DeSnapper
)

fakeroot dpkg-deb --build desnapper

rm -rf desnapper/usr/lib

git clone --branch v20181111 https://github.com/diff-match-patch-python/diff-match-patch.git diff-match-patch-20181111

(
  cd diff-match-patch-20181111

  python3 setup.py build
  mkdir -p ../diff-match-patch/usr/lib/python3/dist-packages/
  mv build/lib/diff_match_patch ../diff-match-patch/usr/lib/python3/dist-packages/
)

fakeroot dpkg-deb --build diff-match-patch

rm -rf diff-match-patch-20181111
rm -rf diff-match-patch/usr

git clone --branch v0.3.0 https://github.com/timonwong/sxsdiff sxsdiff-0.3.0

(
  cd sxsdiff-0.3.0

  python3 setup.py build
  mkdir -p ../sxsdiff/usr/lib/python3/dist-packages/
  mv build/lib/sxsdiff ../sxsdiff/usr/lib/python3/dist-packages/
)

fakeroot dpkg-deb --build sxsdiff

rm -rf sxsdiff-0.3.0
rm -rf sxsdiff/usr
