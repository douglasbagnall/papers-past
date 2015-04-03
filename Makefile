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
