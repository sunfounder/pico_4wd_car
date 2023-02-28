.. _install_micropython_on_pico:

2. Install MicroPython on Your Pico(Optional)
==================================================

.. warning::
    Since we have already installed the MicroPython firmware and related libraries for the Raspberry Pi Pico at the factory. So this step and the previous step can be skipped. But it is okay to follow the process if you want to.


MicroPython is a software implementation of a programming language largely compatible with Python 3, written in C, that is optimized to run on a microcontroller.

MicroPython consists of a Python compiler to bytecode and a runtime interpreter of that bytecode. The user is presented with an interactive prompt (the REPL) to execute supported commands immediately. Included are a selection of core Python libraries; MicroPython includes modules which give the programmer access to low-level hardware.

* Reference: |link_micropython|


Now come to install MicroPython into Raspberry Pi Pico, Thonny IDE provides a very convenient way for you to install it with one click.



.. note::
    If you do not wish to upgrade Thonny, you can use the Raspberry Pi official |link_micropython_pi| by dragging and dropping an ``rp2_pico_xxxx.uf2`` file into Raspberry Pi Pico.



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


Congratulations, now your Raspberry Pi Pico is ready to go.