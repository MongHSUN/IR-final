build ?= n
all:
	@# query.py usage: python3 query.py url queryTermNum
	@# main program usage: ./main -f file_list -v vocab -i invIndex -q query -t topResult
#make build='y' can rebuild database
ifeq ($(build),y)	
	python3 file.py ../data/lrcc
	python3 build_term.py
endif
	#make URL="..."
	g++ main.cpp -o main
	python3 query.py ${URL} 20 > ../data/query
	./main -f ../data/file_list -v ../data/vocab -i ../data/invIndex -q ../data/query -t 15 > ../data/result
	python3 youtube.py -t
