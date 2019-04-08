all:
	python apriori.py $(p) $(s) $(d)
pypy:
	pypy apriori.py $(p) $(s) $(d)
1k_demo:
	python apriori3.py ./APhw_demo/T10I10N0.1KD1K.data 4 0
10k_demo:
	python apriori3.py ./APhw_demo/T20I15N1KD10K.data 9 0
100k_demo:
	python apriori3.py ./APhw_demo/T12I30N0.5KD100K.data 300 0
500k_demo:
	python apriori.py ./APhw_demo/T18I20N2KD5000K.data 65000 0
1k:
	python apriori3.py ./AP/T15I7N0.5KD1K.data 5 0
1k_profilling:
	python -m cProfile -o profile.pstats apriori2.py ./AP/T15I7N0.5KD1K.data 5 0
10k:
	python apriori3.py ./AP/T15I7N0.5KD10K.data 50 0
1000k:
	python apriori3.py ./AP/T15I7N0.5KD1000K.data 30000 0
png:
	python -m gprof2dot -f pstats profile.pstats | dot -T png -o profile.pn

