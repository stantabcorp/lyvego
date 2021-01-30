CC=python3
pip=-m pip install
update:
	$(CC) $(pip) -r requirements.txt
upgrade:
	$(CC) $(pip) -r requirements.txt --upgrade
install:
	apt install python3 && apt install python3-pip