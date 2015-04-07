all:: books

.PRECIOUS: books books/chapters

books/chapters: books
	mkdir -p $@
	./split-books-into-chapters $^/*

books:
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
