Motor Calibration
=================

Because of assembly methods and other reasons, your motor may still need a calibration direction. Otherwise, when the car moves forward, it may turn left, turn right, or even go backwards. Please follow the following steps to complete the calibration.

**How to do？**

#. Select Correct Interpreter. Plug the Pico into your computer with a micro USB cable and select the "MicroPython (Raspberry Pi Pico).COMXX" interpreter in the bottom right corner.

    .. image:: img/sec_inter.png


#. Go to the ``pico_4wd_car/examples`` path and double click on ``move_forward.py`` to open it. 这是一个非常简单的示例，它会让小车往前走。

    .. image:: img/move_forward.png

#. Observe whether the wheels of the car are driving forward and marked the wrong motor.

#. Open the ``pico_4wd.py`` file that was uploaded to the pico before, modify the wrong motor's ``dir`` to reverse the value and save it.

    .. image:: img/rdp_dir.png

#. Run again ``move_Forward.py``, if the car is driving correctly, the calibration is completed.
