.PHONY: split

split:
	tar xzf reports/reports_nov1_2018.tar.gz
	./split-reports.py
