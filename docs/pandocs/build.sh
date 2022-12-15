echo "Creating html documentation at index.html..."
pandoc index.md -f markdown -t html -s -o output/index.html --metadata title="explicatio"
echo "Creating pdf documentation at index.pdf..."
pandoc index.md -s -o output/index.pdf
echo "Creating man page at explicatio..."
pandoc -s -t man man.md -o output/explicatio.1
echo "Installing man page. You may be prompted for a password..."
sudo cp output/explicatio.1 /usr/local/share/man/man1