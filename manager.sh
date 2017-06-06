# !/bin/bash

clear
echo "Clean source directory of existing content"
mv source/index.html.md source/index.html.md.OLD
rm source/*.md
mv source/index.html.md.OLD source/index.html.md
echo "GSheets Content Generation"
python pulldown.py
echo "Middleman - Build"
middleman build
echo "Middleman - Deploy"
middleman deploy
