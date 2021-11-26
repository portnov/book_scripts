Djvu-tools README
=================

This repo contains a set of scripts to deal with DJVU files.

Prerequisites
-------------

This set of scripts uses commands from djvulibre package.

djvu2tiff
---------

Usage:
  
    djvu2tiff INPUT.DJVU OUTPUT.TIFF

This creates a multipage TIFF file from DJVU file.

tiffs2djvu
----------

Usage:
  
    tiffs2djvu DIRECTORY OUTPUT.DJVU

where DIRECTORY is a directory with (single-page) TIFF files.

prepare_bookmarks.py
--------------------

This script is aimed to simplify bookmarks creation for DJVU files. Djvulibre's djvused program uses the following format of bookmarks:

    (bookmarks
     ("1 first chapter" "#10" 
       ("1.1 first section" "#11" 
         ("1.1.1 first subsection" "#12" )
       )
       ("1.2 second section" "#13" )
     )
     ("2 second chapter" "#14" 
       ("2.1 first section" "#16" )
       ("2.2 second section" "#17" )
     )
    )

This format is not very user-friendly. `prepare_bookmarks.py` script converts the following simpler format into Djvulibre's format:


    1 first chapter #10
      1.1 first section #11
        1.1.1 first subsection #12
      1.2 second section #13
    2 second chapter #14
      2.1 first section #16
      2.2 second section #17

Hierarchy is defined by indents. Page numbers are placed after `#` sign.

Usage:

    prepare_bookmarks.py BOOKMARKS.INPUT > BOOKMARKS.OUTPUT

djvu-embed-bookmarks.sh
-----------------------

This is a wrapper script around djvused to add bookmarks to DJVU file. Usage:

    djvu-embed-bookmarks.sh INPUT.DJVU BOOKMARKS.TXT

where BOOKMARKS.TXT is a file with bookmarks in Djvulibre's format.

tesseract-djvu.sh
-----------------

This script is a wrapper for Tesseract OCR, to recognize text from DJVU files. Usage:

    tesseract-djvu.sh INPUT.DJVU PAGESPEC [TESSERACTOPTS]

For example:

    tesseract-djvu.sh Input.djvu 3-5,10-12 -l rus

