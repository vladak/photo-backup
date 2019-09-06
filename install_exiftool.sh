#!/bin/bash

if [[ $OS == "macOS" ]]; then
	brew install exiftool
elif [[ $OS == "Linux" ]]; then
	sudo apt-get install -qq exiftool
else
	echo "Unknown OS: $OS"
	exit 1
fi
