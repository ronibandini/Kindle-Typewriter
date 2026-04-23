<img width="200" height="125" alt="logosmall" src="https://github.com/user-attachments/assets/0a807c01-0562-45e9-85be-d595bab68cae" />

# Kindle-Typewriter
Convert your Kindle Paperwhite jailbreaked into a Typewriter

# Parts
Kindle Paperwhite (Jailbreaked)
Adafruit Thermal Printer
Raspberry Pi Zero W
Female female jumper cables
5v 3A Power Supply

# Circuit
<img width="940" height="788" alt="Circuito" src="https://github.com/user-attachments/assets/96e97422-32ea-42a0-a4ad-d861202fcf9e" />

Pin 8 (TXD / GPIO 14)	RX
Pin 10 (RXD / GPIO 15)	TX 

# Software setup

In Raspberry Pi Zero W
pip install pyserial flask --break-system-packages
pip install python-escpos --break-system-packages
raspi-confi, enable serial
Upload kindletypewriter.py
python kindletypewriter.py

In the Kindle
Copy the .sh as you copy a book
Start kterm
chmod +x kindletypewriter.sh
bash kindletypewriter.sh
