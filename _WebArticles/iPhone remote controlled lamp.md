# iPhone remote controlled lamp

_Captured: 2015-11-14 at 10:59 from [m.instructables.com](http://m.instructables.com/id/iPhone-remote-controlled-lamp/?ALLSTEPS)_

[ ![Picture of iPhone remote controlled lamp](http://cdn.instructables.com/FBV/QTG9/HY8ILEWV/FBVQTG9HY8ILEWV.MEDIUM.jpg) ](http://www.instructables.com/file/FBVQTG9HY8ILEWV/)

> _[Picture of iPhone remote controlled lamp](http://www.instructables.com/file/FBVQTG9HY8ILEWV/)_ 

![iPhone remote controlled lamp](http://cdn.instructables.com/FBV/QTG9/HY8ILEWV/FBVQTG9HY8ILEWV.SQUARE2.jpg)

#### Intro: iPhone remote controlled lamp

This project uses the iPhone and a raspberry pi to remote control the lamp. Both the iPhone and the raspberry pi are connected to the wifi router. The ...

1 

![System diagram](http://cdn.instructables.com/FN1/V7YX/HY8ILGHI/FN1V7YXHY8ILGHI.SQUARE2.jpg)

#### Step 1: System diagram

The system diagram is shown in this figure. The data flow is straightforward. The iPhone is connected to the wifi router wirelessly while the Raspberry pi is connected ...

2 

![Electronics](http://cdn.instructables.com/FUJ/CEK9/HY8ILEUA/FUJCEK9HY8ILEUA.SQUARE2.jpg)

#### Step 2: Electronics

Here are the electronics parts. 1. A Raspberry pi board2. A relay board3. A universal board for connecting the Raspberry pi and the relay board4. A lamp5. A ...

3 

![Circuit](http://cdn.instructables.com/FLK/RTTK/HY8ILGGT/FLKRTTKHY8ILGGT.SQUARE2.jpg)

#### Step 3: Circuit

Since the output voltage of the Raspberry pi is 3.3V and the control signal voltage of the relay board is 5V, we need to change the 3.3V signal ...

4 

![Software-Raspberry Pi](http://www.instructables.com/static/defaultIMG/default.SQUARE2.png)

#### Step 4: Software-Raspberry Pi

Some modification of the Raspberry pi is needed to perform this project's task.1. Auto login2. Static IP3. Auto-run script4. GPIO control5. Socket serverDetails are list below:1. Auto loginedit ...

5 

![Software-iPhone](http://www.instructables.com/static/defaultIMG/default.SQUARE2.png)

#### Step 5: Software-iPhone

Pythonista is installed in the iPhone to run the Python script, it also provides an UI design function.. The script is attahed as lamp.py. Introduction of Pythonista can ...

6 

![Connection and Testing](http://cdn.instructables.com/FNI/X460/HY8ILEWG/FNIX460HY8ILEWG.SQUARE2.jpg)

#### Step 6: Connection and Testing

1\. modify the lamp, break the live wire and connect into the relay board, one end connect to the com port, and another end connect to the normal ...

[ ![Picture of iPhone remote controlled lamp](http://cdn.instructables.com/FBV/QTG9/HY8ILEWV/FBVQTG9HY8ILEWV.MEDIUM.jpg) ](/file/FBVQTG9HY8ILEWV/)

Show All Items  
__

This project uses the iPhone and a raspberry pi to remote control the lamp. Both the iPhone and the raspberry pi are connected to the wifi router. The lamp on/off commands are sent from iPhone and received by the raspberry pi embedded system. Then the raspberry pi triggers the IO to control the lamp through a relay. The lamp can be replaced by other home appliances. The software is written in Python and it can be easily port to other devices.

## Step 1: System diagram

[ ![Picture of System diagram](http://cdn.instructables.com/FN1/V7YX/HY8ILGHI/FN1V7YXHY8ILGHI.MEDIUM.jpg) ](/file/FN1V7YXHY8ILGHI/)

Show All Items  
__

The system diagram is shown in this figure. The data flow is straightforward. The iPhone is connected to the wifi router wirelessly while the Raspberry pi is connected to the wifi router through a lan cable (this can change to wireless with a wifi adapter installed in the Raspberry pi). One of the Raspberry pi's IO is connected to a relay board. Since the relay board control voltage is 5V and the Raspberry pi output voltage is 3.3V, a transistor is used to perform the voltage transition; the detail will be introduced in step 3. Then the lamp can be controlled through the relay board. 

Both the iPhone and the Raspberry pi need to run a software for communication. In this project, Python is used as the programming language. In iPhone, Pythonista is installed and run the script, a UI is also designed. In Raspberry pi, a Python script is run automatically after booting the system. The communication is based on socket TCP mode. 

## Step 2: Electronics

[ ![Picture of Electronics](http://cdn.instructables.com/FUJ/CEK9/HY8ILEUA/FUJCEK9HY8ILEUA.MEDIUM.jpg) ](/file/FUJCEK9HY8ILEUA/)

[ ![IMG_3456.JPG](/intl_static/img/pixel.png) ![IMG_3456.JPG](http://cdn.instructables.com/FV3/E4ML/HY8ILEYM/FV3E4MLHY8ILEYM.MEDIUM.jpg) ](/file/FV3E4MLHY8ILEYM/)

[ ![IMG_3445.JPG](/intl_static/img/pixel.png) ![IMG_3445.JPG](http://cdn.instructables.com/FPK/IVNJ/HY8ILEV2/FPKIVNJHY8ILEV2.MEDIUM.jpg) ](/file/FPKIVNJHY8ILEV2/)

[ ![IMG_3446.JPG](/intl_static/img/pixel.png) ![IMG_3446.JPG](http://cdn.instructables.com/F7O/04QK/HY8ILEVL/F7O04QKHY8ILEVL.MEDIUM.jpg) ](/file/F7O04QKHY8ILEVL/)

[ ![IMG_3455.JPG](/intl_static/img/pixel.png) ![IMG_3455.JPG](http://cdn.instructables.com/FJG/S1NB/HY8ILEXX/FJGS1NBHY8ILEXX.MEDIUM.jpg) ](/file/FJGS1NBHY8ILEXX/)

[ ![IMG_3459.JPG](/intl_static/img/pixel.png) ![IMG_3459.JPG](http://cdn.instructables.com/FVQ/WSTN/HY9B60NF/FVQWSTNHY9B60NF.MEDIUM.jpg) ](/file/FVQWSTNHY9B60NF/)

[ ![IMG_3460.JPG](/intl_static/img/pixel.png) ![IMG_3460.JPG](http://cdn.instructables.com/F1S/3EJW/HY9B60ND/F1S3EJWHY9B60ND.MEDIUM.jpg) ](/file/F1S3EJWHY9B60ND/)

Show All Items  
__

Here are the electronics parts. 

1\. A Raspberry pi board

2\. A relay board

3\. A universal board for connecting the Raspberry pi and the relay board

4\. A lamp

5\. A wireless router

6\. A USB charger for powering up the Raspberry pi

7\. A transistor 8050

8\. Two resistor (1K ohm)

9\. Lan cable and USB cable and

10\. Of course an iPhone as the remote control

## Step 3: Circuit

[ ![Picture of Circuit](http://cdn.instructables.com/FLK/RTTK/HY8ILGGT/FLKRTTKHY8ILGGT.MEDIUM.jpg) ](/file/FLKRTTKHY8ILGGT/)

Show All Items  
__

Since the output voltage of the Raspberry pi is 3.3V and the control signal voltage of the relay board is 5V, we need to change the 3.3V signal to 5V signal. A voltage converter circuit is shown in this picture. A 8050 transistor is used to perform the transition. When the output GPIO of the Raspberry pi is low, the relay board input signal is high, and the relay is on, the lamp will turn on. When the output GPIO of the Raspberry pi is high, the relay board input signal is low, and the relay is off, the lamp will turn off. 

## Step 4: Software-Raspberry Pi

Some modification of the Raspberry pi is needed to perform this project's task.

1\. Auto login

2\. Static IP

3\. Auto-run script

4\. GPIO control

5\. Socket server

Details are list below:

1\. Auto login

edit /etc/inittab, change 

"1:2345:respawn:/sbin/getty --noclear 38400 tty1" into

"1:2345:respawn:/bin/login -f pi tty1 /dev/tty1 2>&1"

ref: <http://elinux.org/RPi_Debian_Auto_Login>

2\. Static IP

set the IP as "192.168.1.200"

edit /etc/network/interfaces, change

"iface eth0 inet dhcp" into

"iface eth0 inet static

address 192.168.1.200 

netmask 255.255.255.0 

network 192.168.1.0 

broadcast 192.168.1.255 

gateway 192.168.1.1"

ref: [https://www.modmypi.com/blog/tutorial-how-to-give-...](https://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address)

3\. Auto-run script

edit .bashrc, add at the bottom:

"sudo python server_5.py"

server_5.py is the script to serve the lamp control command

ref: [http://www.raspberrypi.org/forums/viewtopic.php?f=...](http://www.raspberrypi.org/forums/viewtopic.php?f=66&t=59960)

4\. GPIO control

in order to contol the IO, RPi.GPIO is installed,

ref: [http://openmicros.org/index.php/articles/94-ciseco...](http://openmicros.org/index.php/articles/94-ciseco-product-documentation/raspberry-pi/217-getting-started-with-raspberry-pi-gpio-and-python)

note: the version is changed to the latest one

5\. Socket server

the Raspberry pi is acting as a socket server

the Python script is attached as server_5.py. 

ref: [http://www.binarytides.com/python-socket-programmi...](http://www.binarytides.com/python-socket-programming-tutorial/)

All the modified files are attached. 

  * [ ![server_5.py](http://www.instructables.com/static/defaultIMG/file.TINY.gif) server_5.py ](/files/orig/FNN/XIR0/HY8ILHW5/FNNXIR0HY8ILHW5.py)
  * [ ![interfaces](http://www.instructables.com/static/defaultIMG/file.TINY.gif) interfaces ](/files/orig/FCN/K26M/HY8ILHWG/FCNK26MHY8ILHWG.null)
  * [ ![.bashrc](http://www.instructables.com/static/defaultIMG/file.TINY.gif) .bashrc ](/files/orig/F0N/0PRE/HY8ILHWX/F0N0PREHY8ILHWX.null)
  * [ ![inittab](http://www.instructables.com/static/defaultIMG/file.TINY.gif) inittab ](/files/orig/FVH/IPL2/HY8ILHXE/FVHIPL2HY8ILHXE.null)

## Step 5: Software-iPhone

[ ![Picture of Software-iPhone](http://cdn.instructables.com/F4E/AVV7/HY8ILEZS/F4EAVV7HY8ILEZS.MEDIUM.jpg) ](/file/F4EAVV7HY8ILEZS/)

[ ![IMG_3441.PNG](/intl_static/img/pixel.png) ![IMG_3441.PNG](http://cdn.instructables.com/F9H/BU5C/HY8ILF09/F9HBU5CHY8ILF09.MEDIUM.jpg) ](/file/F9HBU5CHY8ILF09/)

[ ![IMG_3457.PNG](/intl_static/img/pixel.png) ![IMG_3457.PNG](http://cdn.instructables.com/FMP/MSEQ/HY9B67AJ/FMPMSEQHY9B67AJ.MEDIUM.jpg) ](/file/FMPMSEQHY9B67AJ/)

Show All Items  
__

Pythonista is installed in the iPhone to run the Python script, it also provides an UI design function.. The script is attahed as lamp.py. 

Introduction of Pythonista can be found here: <http://omz-software.com/pythonista/>

  * [ ![lamp.py](http://www.instructables.com/static/defaultIMG/file.TINY.gif) lamp.py ](/files/orig/F8C/8CHI/HY8ILI3U/F8C8CHIHY8ILI3U.py)

## Step 6: Connection and Testing

[ ![Picture of Connection and Testing](http://cdn.instructables.com/FNI/X460/HY8ILEWG/FNIX460HY8ILEWG.MEDIUM.jpg) ](/file/FNIX460HY8ILEWG/)

[ ![IMG_3450.JPG](/intl_static/img/pixel.png) ![IMG_3450.JPG](http://cdn.instructables.com/FCX/0MXJ/HY8ILEXE/FCX0MXJHY8ILEXE.MEDIUM.jpg) ](/file/FCX0MXJHY8ILEXE/)

[ ![IMG_3437.PNG](/intl_static/img/pixel.png) ![IMG_3437.PNG](http://cdn.instructables.com/FAV/R4M8/HY8ILEYT/FAVR4M8HY8ILEYT.MEDIUM.jpg) ](/file/FAVR4M8HY8ILEYT/)

[ ![IMG_3438.PNG](/intl_static/img/pixel.png) ![IMG_3438.PNG](http://cdn.instructables.com/F9A/2BKD/HY8ILEZ4/F9A2BKDHY8ILEZ4.MEDIUM.jpg) ](/file/F9A2BKDHY8ILEZ4/)

[ ![IMG_3439.PNG](/intl_static/img/pixel.png) ![IMG_3439.PNG](http://cdn.instructables.com/FPM/4TY9/HY8ILEZD/FPM4TY9HY8ILEZD.MEDIUM.jpg) ](/file/FPM4TY9HY8ILEZD/)

[ ![IMG_3458.PNG](/intl_static/img/pixel.png) ![IMG_3458.PNG](http://cdn.instructables.com/FQ7/XL7B/HY9B60Q8/FQ7XL7BHY9B60Q8.MEDIUM.jpg) ](/file/FQ7XL7BHY9B60Q8/)

Show All Items  
__

1\. modify the lamp, break the live wire and connect into the relay board, one end connect to the com port, and another end connect to the normal open port. 

2\. use the GPIO 11 of the Raspberry pi to control the relay

3\. connect the iPhone and the Raspberry pi to the wifi router

4\. the screen of the iPhone is captured after running the script, there will be pop-up notifications after press On and Off buttons. 

5\. two demo videos are also embedded 

It can be easily modified to control other home appliances. And it is quite convenient since you can control it everywhere when you can receive the wifi signal. 

<p>nice work</p><p>http://www.sayfakutusu.com bedava firma kayıt &uuml;cretsiz web sitesi oluşturma ve firma rehberi</p>

<p>Thanks!</p>

<p>well done!</p>

<p>Thanks!</p>

<p>Nice job! That light is super pretty too!</p>

<p>Thanks!</p>
