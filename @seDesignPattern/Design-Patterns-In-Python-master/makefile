# Builds the e-book in multiple formats

OPTIONS = -s --toc --toc-depth=2 --highlight-style haddock 
SOURCE_NAME = Design_Patterns_In_Python
OUTPUT_NAME = Output/Design_Patterns_In_Python

#==============================================================================
all: $(OUTPUT_NAME).epub $(OUTPUT_NAME).pdf $(OUTPUT_NAME).html FAKE_IMAGES
	@echo -e "All made"

#==============================================================================
$(OUTPUT_NAME).html: $(SOURCE_NAME).md
	@mkdir -p Output
	@echo -e "Making html."
	pandoc $< $(OPTIONS) -o $@
	@echo -e "html made.\n"

#==============================================================================
$(OUTPUT_NAME).pdf: $(SOURCE_NAME).md
	@mkdir -p Output
	@echo -e "Making pdf."
	pandoc $< $(OPTIONS) -o $@
	@echo -e "pdf made.\n"

#==============================================================================
$(OUTPUT_NAME).epub: $(SOURCE_NAME).md
	@mkdir -p Output
	@echo -e "Making epub."
	pandoc $< $(OPTIONS) -o $@
	@echo -e "epub made.\n"

FAKE_IMAGES: 
	@cp -r Images Output/
	@echo "Images copied."

#==============================================================================
clean: FRC
# remove the temporary files
	@rm -f *.pdf *.pyc *.html *.epub
	@echo "Removed all: pdfs, html, epubs and temp files."

#==============================================================================
#D Pseudo target causes all targets that depend on FRC to be remade even in 
#D case a file with the name of the target exists. Works unless there is a file
#D called FRC in the directory.
#------------------------------------------------------------------------------
FRC: