Getting Started with MicroPython
==================================

MicroPython is a full Python compiler and runtime that runs on the microcontroller's hardware like Raspberry Pi Pico. 
The user is presented with an interactive prompt (the REPL) to excute supported commands immediately. 
Included are a selection of core Python libraries; MicroPython includes modules which give the programmer access to low-level hardware.

* Reference: `MicroPython - Wikipedia <https://en.wikipedia.org/wiki/MicroPython>`_

The Story Starts Here
--------------------------------

Everything changed in 2013 when Damien George launched a crowdfunding campaign (Kickstarter).

Damien was an undergraduate student at Cambridge University and an avid robotics programmer. He wanted to reduce the world of Python from a gigabyte machine to a kilobyte. His Kickstarter campaign was to support his development while he turned his proof of concept into a finished implementation.

MicroPython is supported by a diverse Pythonista community that has a keen interest in seeing the project succeed.

In addition to testing and supporting the code base, the developers provided tutorials, code libraries, and hardware ports, making the project far more than Damien could have done alone.

* Reference: `realpython <https://realpython.com/micropython/>`_

Why MicroPython？
------------------

Although the original Kickstarter campaign released MicroPython as a development board "pyboard" with STM32F4, MicroPython supports many ARM-based product architectures. The mainline supported ports are ARM Cortex-M (many STM32 boards, TI CC3200/WiPy, Teensy boards, Nordic nRF series, SAMD21 and SAMD51), ESP8266, ESP32, 16bit PIC, Unix, Windows, Zephyr and JavaScript.
Second, MicroPython allows for fast feedback. This is because you can use REPL to enter commands interactively and get responses. You can even tweak code and run it immediately instead of traversing the code-compile-upload-execute cycle.

While Python has the same advantages, for some Microcontroller boards like the Raspberry Pi Pico, they are small, simple and have little memory to run the Python language at all. That's why MicroPython has evolved, keeping the main Python features and adding a bunch of new ones to work with these Microcontroller boards.

Next you will learn to install MicroPython into the Raspberry Pi Pico.

* Reference: `MicroPython - Wikipedia <https://en.wikipedia.org/wiki/MicroPython>`_
* Reference: `realpython <https://realpython.com/micropython/>`_

Installing MicroPython
------------------------------


#. Press and hold the **BOOTSEL** button and connect the Pico to the computer with a Micro USB cable.
#. Release the BOOTSEL button after your Pico is mount as a Mass Storage Device called RPI-RP2.

    .. image:: img/bootsel_onboard.png

#. Open the drive, you'll see two files on your Pico: **INDEX.HTM** and **INFO_UF2.TXT**. Double click the first file, INDEX.HTM, to open it in your browser.

    * **INDEX.HTM** : This is a welcome page telling you all about your Pico.
    * **INFO_UF2.TXT** : Contains the version of the bootloader it's currently running.

        .. image:: img/index_htm.png

#. When the browser opens, click **Getting started with MicroPython** .

    .. image:: img/welcome_pico.png

#. Download the MicroPython firmware by clicking the **Download UF2 file** button.

    .. image:: img/download_uf2.png

#. Open the **Downloads** folder and find the file you just downloaded - it will be called 'pico_micropython_xxxx.uf2', then drag it to **RPI-RP2** storage drive. Your Pico will reboot and disappear from the File Manager.

    .. image:: img/move_uf2.png

.. note::

    Please ignore the warning that a drive was removed without being ejected, that's supposed to happen!
    
    When you dragged the MicroPython firmware file onto your Pico, you told it to flash the firmware onto its internal storage.
    To do that, your pico switches out of the special mode you put it in with the 'BOOTSEL' button, flashes the new firmware, and then load it (meaning that your Pico is now running MicroPython).

Congratulations: your're now ready to get started with MicroPython on your Raspberry Pi Pico!