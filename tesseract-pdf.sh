#!/bin/bash

if [[ $# -lt 2 ]]
then echo "Synopsis: tesseract-pdf.sh INPUT.PDF PAGESPEC [TESSERACTOPTS]"
     echo "    where PAGESPEC specifies pages to be recognized, like 10-15, in pdftk's format"
     echo "          TESSERACTOPTS are options to be passed to tesseract, such as: -l rus"
     exit 1
fi

PDF=$(realpath "$1")
shift
PAGES=$1
shift
TESSERACTOPTS=$@

BASE=$(basename "$PDF" .pdf)

DIR=$(mktemp -d)
pushd $DIR

pdftk "$PDF" cat $PAGES output pages.pdf
pdftocairo -tiff pages.pdf

ls pages-*.tif | while read TIF
do tesseract $TESSERACTOPTS $TIF - >> output.txt
done

popd

mv $DIR/output.txt "$BASE.txt"
rm -rf $DIR

