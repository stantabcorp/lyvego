CC=python3
pip=-m pip install
update:
	$(CC) $(pip) -r requirements.txt
upgrade:
	$(CC) $(pip) -r requirements.txt --upgrade
install:
	sudo apt install python3-dev python3-pip