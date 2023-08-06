#!/bin/bash

# Check if a filename was provided as argument
if [ $# -eq 0 ]; then
    echo "Please provide a filename as argument"
    exit 1
fi

# Set the input file name
INPUT_ADOC=$1

# Convert the AsciiDoc file to DocBook format
docbook=$(asciidoctor --backend docbook --out-file - $INPUT_ADOC)

# Convert the DocBook file to Microsoft Word format
pandoc --from docbook --to docx --output ${INPUT_ADOC%.*}.docx <<< "$docbook"

# Open the converted Word document
open ${INPUT_ADOC%.*}.docx
