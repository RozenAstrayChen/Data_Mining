all:
	python apriori.py $(p) $(s) $(d)
pypy:
	pypy apriori.py $(p) $(s) $(d)
1k_demo:
	python apriori.py ./APhw_demo/T10I10N0.1KD1K.data 4
10k_demo:
	python apriori.py ./APhw_demo/T20I15N1KD10K.data 9
100k_demo:
	python apriori.py ./APhw_demo/T12I30N0.5KD100K.data 300
500k_demo:
	python apriori.py ./APhw_demo/T18I20N2KD5000K.data 65000
1k:
	python apriori.py ./AP/T15I7N0.5KD1K.data 5 0
10k:
	python apriori.py ./AP/T15I7N0.5KD10K.data 50
1000k:
	python apriori.py ./AP/T15I7N0.5KD1000K.data 30000

