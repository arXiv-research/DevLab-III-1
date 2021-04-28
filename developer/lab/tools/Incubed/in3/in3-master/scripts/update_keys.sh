#!/bin/sh
DST=../c/src/core/util/used_keys.h
echo "// this is a autogenerated file (scripts/updqate_keys.sh)! Do not edit manually!\nstatic char* USED_KEYS[] = {" > $DST
echo "">tmp
for f in `find ../c/src -name "*.c" -o -name "*.h"`
do
  echo "check $f"
  cat $f | grep "key(\"" | sed 's/.*key("\([^"]*\)").*/    "\1\",/' >> tmp
done
sort tmp | uniq >> $DST 
echo "    0};" >> $DST
rm -f tmp