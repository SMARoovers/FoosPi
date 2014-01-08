How to install FoosPi

Prerequisites:

```
sudo apt-get update
sudo apt-get install python
sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio
cd /tmp
wget https://pypi.python.org/packages/source/R/RPi.GPIO/RPi.GPIO-0.5.4.tar.gz
tar zxvf RPi.GPIO-0.5.4.tar.gz
cd RPi.GPIO-0.5.4
sudo python setup.py install
cd /tmp
rm RPi.GPIO-0.5.4.tar.gz
rm -r RPi.GPIO-0.5.4
```

Install FoosPi:

Go to the location to where you want to install FoosPi, for example /home/pi

```
cd /home/pi
git clone https://github.com/SMARoovers/FoosPi.git
cd /home/pi/FoosPi
```

Update FoodPi:

Go to the FoosPi folder


```
git pull origin
```