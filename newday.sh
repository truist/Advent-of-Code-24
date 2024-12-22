#!/usr/bin/env bash

set -e

if [[ $# -ne 2 ]]; then
	echo "args: <day string> <python file basename>" >&2
	exit 1
fi

daystr="$1"
pyname="$2"

mkdir -p "$daystr"

touch "$daystr/test.txt"
touch "$daystr/input.txt"

cp template/template.py "$daystr/$pyname.py"
sed -i ""  "s/NEWDAY/$daystr/g" "$daystr/$pyname.py"

cd "$daystr"
vim "$pyname.py" test.txt input.txt

