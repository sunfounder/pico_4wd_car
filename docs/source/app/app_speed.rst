3. APP - SPEED
==================

In this project, you can view the speed and mileage of the car's movement on the app.

**Quick User Guide**

#. Run the ``app_3_speed.py`` file under the ``pico_4wd_car\examples\app_control`` path.

#. Based on :ref:`app_move`, add **Gauge** and **Number** widgets to the **B** and **C** areas as shown below.

    .. image:: img/APP_DB_3_1.png

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. Now, tap on the **D-Pad** to control the movement and adjust the power via the **Throttle** widget. You can also see the speed and mileage from the **B** and **C** areas.

**How it works?**

This project is generally the same as :ref:`app_move`, except that two lines have been added to the ``on_receive(data)`` function to send the APP the speed and mileage data.


.. code-block:: python
    :emphasize-lines: 10,12

    '''----------------- on_receive (ws.loop()) ---------------------'''
    def on_receive(data):
        global throttle_power, steer_power, move_status, dpad_touched

        ''' if not connected, skip & stop '''
        if not ws.is_connected():
            return

        # Speed measurement
        ws.send_dict['B'] = round(speed.get_speed(), 2) # uint: cm/s
        # Speed mileage
        ws.send_dict['C'] = speed.get_mileage() # unit: meter

        # ..........