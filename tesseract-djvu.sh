#!/bin/bash -x

if [[ $# -lt 2 ]]
then echo "Synopsis: tesseract-djvu.sh INPUT.DJVU PAGESPEC [TESSERACTOPTS]"
     echo "    where PAGESPEC specifies pages to be recognized, like 10-15,20-30"
     echo "          TESSERACTOPTS are options to be passed to tesseract, such as: -l rus"
     exit 1
fi

DJVU=$1
shift
PAGES=$1
shift
TESSERACTOPTS=$@

DIR=$(mktemp -d)
BASE=$(basename "$DJVU" .djvu)

ddjvu -format=tiff "$DJVU" -page=$PAGES $DIR/pages.tiff

tesseract $TESSERACTOPTS $DIR/pages.tiff "$BASE"

rm -rf $DIR
