all:: books/chapters

.SECONDARY: books/chapters books/all books/merged

books/chapters: books/merged
	mkdir -p $@
	./split-books-into-chapters $^/*


books/merged: books/all
	mkdir -p $@
	./merge-books mergers $^ $@

books/all:
	mkdir -p $@
	./extract-nzetc-text corpus/nzetc/*.xml
	./fix-archive-text corpus/archive/*.txt
	./fix-archive-text corpus/gutenberg/*.txt
	./fix-archive-text corpus/misc/*.txt

recur:
	git clone https://github.com/douglasbagnall/recur.git

recur/local.mak: recur
	@echo OK, there is a manual step here.
	@echo ================================
	@echo You need to create a file called 'local.mak' in the recur
	@echo directory. If you are using x86_64, you can just copy or
	@echo symlink 'local.mak.example.x86_64'  -- otherwise try using
	@echo that as a template.
	@echo
	@echo "cd recur && ln -s local.mak.example.x86_64 local.mak"

recur/charmodel.so: recur/local.mak
	cd recur && git pull
	cd recur && make charmodel.so

charmodel.so: recur/charmodel.so
	ln -s $^ $@

pgm-clean:
	rm -r images
	mkdir images

.PHONY: all pgm-clean

report/reference-corpus.md: dump-corpus-metadata books/all report/appendix-header.md
	cat report/appendix-header.md > $@
	echo >> $@
	./dump-corpus-metadata books/all/ >> $@

#Estimates of good, bad, and mediocre OCR, courtesy of Emerson Vandy.
GOOD_PAPERS = '^(?:AMBPA|AG|CL|TC|DOM|EP|FS|GRA|HNS|IT|LWM|MS|MT|NA|ODT|TS|SUNCH|TPT|WC)_'
# it turns out there are no mediocre papers in the corpus
MEDIOCRE_PAPERS = '^(?:ME|NEM|NZH|OAM|OSWCC|PBH|ST|WT|WAG|WDT|WH|WCT)_'
BAD_PAPERS = '^(?:AS|NOT|BOPT|HAST|THD|HC|MEX|TDN|THS)_'


articles/done:
	mkdir -p $(@D)
	./parse-json --nuke-double-space --id-filter-re=$(GOOD_PAPERS) json/*.json
	touch $@

bad-articles/done:
	mkdir -p $(@D)
	./parse-json --nuke-double-space --id-filter-re=$(BAD_PAPERS) json/*.json --dest $(@D)
	touch $@


low-noise/done: articles/done
	mkdir -p $(@D)
	for x in {0..4095}; do \
	  d=$$(printf '%03x' $$x); \
	  mkdir $(@D)/$$d; \
	  grep -rL '°' $(<D)/$$d | xargs cp -lt $(@D)/$$d; \
	done
	touch $@

sample/raw-good.txt:
	mkdir -p $(@D)
	./parse-json --nuke-double-space --raw-sample=1000000 \
	    --id-filter-re=$(GOOD_PAPERS) json/*.json > $@

sample/raw-bad.txt:
	mkdir -p $(@D)
	./parse-json --nuke-double-space --raw-sample=1000000 \
	    --id-filter-re=$(BAD_PAPERS) json/*.json > $@
