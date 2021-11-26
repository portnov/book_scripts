Book-Scripts README
===================

This repo contains a set of scripts to deal with DJVU or PDF files.

Prerequisites
-------------

This set of scripts uses commands from:

* djvulibre package
* pdftk toolkit
* Tesseract OCR.

Python scripts require Python 3.9+.

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

This script is aimed to simplify bookmarks creation for DJVU or PDF files.

It takes the following simplistic format as input:

    1 first chapter #10
      1.1 first section #11
        1.1.1 first subsection #12
      1.2 second section #13
    2 second chapter #14
      2.1 first section #16
      2.2 second section #17

Hierarchy is defined by indents. Page numbers are placed after `#` sign.

It can output bookmarks in format used by Djvulibre's djvused program:

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

Or, it can output format used by pdftk toolkit:

    BookmarkBegin
    BookmarkTitle: 1 first chapter
    BookmarkLevel: 1
    BookmarkPageNumber: 10
    BookmarkBegin
    BookmarkTitle: 1.1 first section
    BookmarkLevel: 2
    BookmarkPageNumber: 11
    BookmarkBegin
    BookmarkTitle: 1.1.1 first subsection
    BookmarkLevel: 3
    BookmarkPageNumber: 12
    BookmarkBegin
    BookmarkTitle: 1.2 second section
    BookmarkLevel: 2
    BookmarkPageNumber: 13
    BookmarkBegin
    BookmarkTitle: 2 second chapter
    BookmarkLevel: 1
    BookmarkPageNumber: 14
    BookmarkBegin
    BookmarkTitle: 2.1 first section
    BookmarkLevel: 2
    BookmarkPageNumber: 16
    BookmarkBegin
    BookmarkTitle: 2.2 second section
    BookmarkLevel: 2
    BookmarkPageNumber: 17

Usage:

    prepare_bookmarks.py [--to DJVU|PDF] [-o OFFSET] BOOKMARKS.INPUT > BOOKMARKS.OUTPUT

djvu-embed-bookmarks.sh
-----------------------

This is a wrapper script around djvused to add bookmarks to DJVU file. Usage:

    djvu-embed-bookmarks.sh INPUT.DJVU BOOKMARKS.TXT

where BOOKMARKS.TXT is a file with bookmarks in Djvulibre's format.

pdf-embed-bookmarks.sh
----------------------

This script can be used to embed bookmarks into PDF file. Usage:

  pdf-embed-bookmarks.sh INPUT.PDF BOOKMARKS.TXT OUTPUT.PDF [-o offset]

where BOOKMARKS.TXT is in input format for prepare_bookmarks.py.

tesseract-djvu.sh
-----------------

This script is a wrapper for Tesseract OCR, to recognize text from DJVU files. Usage:

    tesseract-djvu.sh INPUT.DJVU PAGESPEC [TESSERACTOPTS]

For example:

    tesseract-djvu.sh Input.djvu 3-5,10-12 -l rus

