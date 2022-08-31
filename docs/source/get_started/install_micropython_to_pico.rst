.. _install_micropython_on_pico:

2. Install MicroPython on Your Pico
==========================================

MicroPython is a full implementation of the Python 3 programming language that runs directly on embedded hardware like Raspberry Pi Pico. You get an interactive prompt (the REPL) to execute commands immediately via USB Serial, and a built-in filesystem. The Pico port of MicroPython includes modules for accessing low-level chip-specific hardware.

* Reference: `MicroPython - Wikipedia <https://en.wikipedia.org/wiki/MicroPython>`_

Now to install MicroPython for Raspberry Pi Pico, Raspberry Pi officially provides a |link_micropython_pi|, by dragging ``rp2_pico_xxxx.uf2`` onto the Pico to complete the installation of MicroPython.


Thonny provides a simpler way, the tutorial is as follows

#. Open Thonny IDE.

    .. image:: img/set_pico1.png

#. Press and hold the **BOOTSEL** button and then connect the Pico to computer via a Micro USB cable. Release the **BOOTSEL** button after your Pico is mount as a Mass Storage Device called **RPI-RP2**.

    .. image:: img/bootsel_onboard.png

#. In the bottom right corner, click the interpreter selection button and select **Install Micropython**.

    .. note::
        If your Thonny does not have this option, please update to the latest version.

    .. image:: img/set_pico2.png

#. In the **Target volume**, the volume of the Pico you just plugged in will automatically appear, and in the **Micropython variant**, select **Raspberry Pi.Pico/Pico H**.

    .. image:: img/set_pico3.png

#. Click the **Install** button, wait for the installation to complete and then close this page.

    .. image:: img/set_pico4.png


Now that your Pico is ready to go, you can continue with the following steps.