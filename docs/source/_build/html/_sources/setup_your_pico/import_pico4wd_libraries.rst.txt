Import Pico-4wd Libraries
==================================

Before using Pico-4wd Car, you need to save its related libraries in Raspberry Pi Pico.

1. Click `here <https://github.com/sunfounder/pico_4wd_car.git>`_ to download the Pico-4wd car kit codes. After unzipping the zip file you have downloaded, you will see all the relevant files.

2. Open the Thonny IDE, select the MicroPython (Raspberry Pi Pico) as the interpreter (the Raspberry Pi Pico must be plugged into the computer first). 

    .. image:: img/interepter_micropython.png

3. Click View -> Files.

    .. image:: img/view_files.png

4. Go to the folder where you store the downloaded pico_4wd_car package, find the files ``pico_4wd.py``, ``pico_rdp.py`` , ``ws.py`` under the path pico_4wd_car/libs, then select the three files and right click on them to upload them to the Raspberry Pi Pico.

    .. image:: img/upload_library.png

5. You can see the uploaded files in the Raspberry Pi Pico window.
   
    .. image:: img/upload_pico.png



Trouble Shooting
-----------------------

Q1: NO MicroPython(Raspberry Pi Pico) Interpreter Option on Thonny IDE?

.. image:: img/interepter_micropython.png


* Check that your Pico is plugged into your computer via a USB cable.
* Check that you have installed MicroPython for Pico (:ref:`Installing MicroPython`).
* The Raspberry Pi Pico interpreter is only available in version 3.3.3 or higher version of Thonny. If you are running an older version, please update (:ref:`Thonny Python IDE`).
* Plug in/out the micro USB cable sveral times.

Q2: Cannot open Pico code or save code to Pico via Thonny IDE?

.. image:: img/save_to_pico.png

* Check that your Pico is plugged into your computer via a USB cable.
* Check that you have selected the Interpreter as **MicroPython (Raspberry Pi Pico)**.

