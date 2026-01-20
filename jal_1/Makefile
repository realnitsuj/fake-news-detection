PANDOC=pandoc

rapport.pdf: ../metadata.yaml *.md
	$(PANDOC) --pdf-engine=lualatex --highlight-style=tango --metadata-file=../metadata.yaml *.md -o ../output/Jalon1.pdf --title "Atelier 3 : Cyber défense dans les réseaux"
