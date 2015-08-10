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

reference-corpus.md: dump-corpus-metadata books/all
	echo '# Books used in the reference corpus' > $@
	echo >> $@
	./dump-corpus-metadata books/all/ >> $@

articles/done:
	mkdir -p $(@D)
	./parse-json --nuke-double-space json/*.json
	touch $@

low-noise/done: articles/done
	mkdir -p $(@D)
	for x in {0..4095}; do \
	  d=$$(printf '%03x' $$x); \
	  mkdir $(@D)/$$d; \
	  grep -rL '°' $(<D)/$$d | xargs cp -lt $(@D)/$$d; \
	done
	touch $@
