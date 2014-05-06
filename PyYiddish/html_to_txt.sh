#!/bin/sh

OCRDIR=mt-materials/ocr_docs
TXTDIR=mt-materials/unclean_txt

for f in `ls $OCRDIR`; do
	echo $f
	pref=${f%.html}
	lynx -dump $OCRDIR/$f > $TXTDIR/"$pref".txt
done
