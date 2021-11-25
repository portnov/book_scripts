#!/bin/bash

set -e

if [[ $# -lt 2 ]]
then echo "Synopsis: djvu-embed-bookmarks.sh INPUT.DJVU BOOKMARKS.TXT"
     cat <<EOT

Bookmarks file format:

(bookmarks
 ("1 first chapter" "#10" 
   ("1.1 first section" "#11" 
     ("1.1.1 first subsection" "#12" )
   )
   ("1.2 second section" "#13" )
 )
 ("2 second chapter" "#14" 
   ("2.1 first section" "#16" )
   ("2.2 second section" "#13" )
 )
)
EOT
     exit 1
fi

DJVU=$1
BOOKMARKS=$2
DSED=$(mktemp)

echo "select; remove-ant; remove-txt; set-outline '$BOOKMARKS'" > $DSED

djvused "$DJVU" -f $DSED -s
