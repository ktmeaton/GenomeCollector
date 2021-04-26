#!/bin/bash

# Update version numbers in executables and build scripts
# Do not put a "v" in front of the version number
# Example Usage:
# ./ver_update.sh v0.6.2 v0.6.3

OLDVER=$1
NEWVER=$2
MODE=$3

FILELIST="setup.py
	  ncbimeta/NCBImeta
	  ncbimeta/NCBImetaAnnotateConcatenate
	  ncbimeta/NCBImetaAnnotateReplace
	  ncbimeta/NCBImetaExport
	  ncbimeta/NCBImetaJoin"

for file in `ls $FILELIST`;
do
    echo "Updating $file from $OLDVER to $NEWVER";
	if [[ $MODE == "sync" ]]; then
		sed -i "s/$OLDVER/$NEWVER/g" $file;
	fi;
done
