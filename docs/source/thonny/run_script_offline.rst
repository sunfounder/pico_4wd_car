.. _run_script_offline:

5. Run Script Offline(Important)
========================================

We can click the |thonny_run| button in Thonny to get the script running in the Raspberry Pi Pico, but this method requires you to connect the Raspberry Pi Pico to your computer with a Micro USB cable.

This method is not very convenient if your Pico 4WD car needs to go on the ground and move around.

So how do you get scripts to work without the USB cable?

An easy way to do this is to save this script as ``main.py`` to the Raspberry Pi Pico.

#. Open Thonny IDE and plug the Pico into your computer with a micro USB cable and click on the "MicroPython (Raspberry Pi Pico).COMxx" interpreter in the bottom right corner.

    .. image:: img/sec_inter.png


#. Open the script first.

    For example, ``app_control.py``.

    If you double click on it, a new window will open on the right.

    .. image:: img/main_open.png

#. Then click **File** -> **Save As**.

    .. image:: img/save_as.png

#. Select **Raspberry Pi Pico** in the pop-up window that appears.

    .. image:: img/save_to_pico.png


#. Set the file name to ``main.py``. If you already have the same file in your Pico, it will prompt to overwrite it.

    .. image:: img/main_name.png

#. Now you can unplug the USB cable, turn on the power switch of Pico-4wd, and Pico-4wd will automatically run this ``main.py`` script.

