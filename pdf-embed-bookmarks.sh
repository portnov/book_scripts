#!/bin/bash

if [[ $# -lt 2 ]]
then echo "Synopsis: pdf-embed-bookmarks.sh INPUT.PDF BOOKMARKS.TXT OUTPUT.PDF"
     exit 1
fi

INPUT=$1
shift
BOOKMARKS=$1
shift
OUTPUT=$1
shift
OPTS="$@"

HERE=$(dirname $0)

INFO=$(mktemp)

pdftk "$INPUT" dump_data_utf8 > $INFO

$HERE/prepare_bookmarks.py -t pdf $OPTS "$BOOKMARKS" >> $INFO

pdftk "$INPUT" update_info_utf8 $INFO output "$OUTPUT"

