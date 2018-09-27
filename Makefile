all:
	python Parent.py &
	python Node.py &
	python sub.py
	
kill:
	pkill python
