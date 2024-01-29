#!/bin/bash
# Check if the number of arguments is exactly 1
if [ "$#" -ne 1 ]; then
	    echo "Usage: $0 <input_file.mp4>"
	        exit 1
fi

# Get the input file name
input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
	    echo "Error: File '$input_file' not found."
	        exit 1
fi

# Check if the file has a .mp4 extension
if [[ "$input_file" != *.mp4 ]]; then
	    echo "Error: Input file must have a .mp4 extension."
	        exit 1
fi

script_dir=$(dirname "$0")
filename=$(basename "$1")

# Extract mp3
ffmpeg -i $input_file -q:a 0 -map a $script_dir/../Src/temp.mp3

# Extract vtt and compose vtt
python3 $script_dir/../Src/VoiceExtract.py

# Add caption to video
ffmpeg -i $input_file -i $script_dir/../Src/temp_compose.vtt -c copy -c:s mov_text  $script_dir/../OutputVideo/caption_$filename

# Remove temp file
rm $script_dir/../Src/temp*
#
