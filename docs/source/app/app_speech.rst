5. Speech
------------------------------

.. warning::
    If you are using an Android device, then you need to change the AP mode in the script to STA mode and download the Google Voice Engine, for a detailed tutorial please refer to :ref:`stt_android`.

The Pico 4WD Car can also be controlled using speech in SunFounder Controller. Pico 4WD Car will perform the set actions based on the commands you say to your mobile device.


**Quick User Guide**

1. Add **Button** widget to **I** area.

    .. image:: img/APP_DB_5_1.png

#. Run the ``app_5_STT.py`` file under the ``pico_4wd_car\examples\app_control`` path.

#. After saving (|app_save|) and connecting (|app_connect|) the controller, click |app_run| to run it.

#. Now tap and hold the **Speech Control(I)** widget and say any of the following commands to see what happens.

    * ``stop``: All movements of the car can be stopped.
    * ``forward``: Let the car move forward.
    * ``backward``：Let the car move backward.
    * ``left``：Let the car turn left.
    * ``right``：Let the car turn right.

**How it works?**

Speech to Text, is where the speech recognition engine on your mobile device recognizes your voice and converts it into text. 
When the data is transferred to the Pico 4WD car, it is already recognized text, such as ``forward`` and so on.



1. During speech recognition, close words may appear, e.g., I say ``forward`` and it recognizes as ``forwhat``, so we define a dictionary to cope with this situation. You can add or modify this dictionary to make Pico 4WD respond to more of your commands.

    .. code-block:: python

        '''------------ Configure Voice Control Commands -------------'''
        voice_commands = {
            # action : [[command , similar commands], [run time(s)]
            "forward": [["forward", "forwhat", "for what"], 3],
            "backward": [["backward"], 3],
            "left": [["left", "turn left"], 1],
            "right": [["right", "turn right", "while", "white"], 1],
            "stop": [["stop"], 1],
        }

#. Recognize the voice command from APP in ``on_receive(data)``.

    .. code-block:: python

        def on_receive(data):
            global current_voice_cmd, voice_start_time, voice_max_time

            ''' if not connected, skip & stop '''
            if not ws.is_connected():
                return

            # Voice control
            voice_text = None
            if 'I' in data.keys() and  data['I'] != '':
                ws.send_dict['I'] = 1
                voice_text = data['I']
            else:
                ws.send_dict['I'] = 0
                
            if voice_text != None:
                print(f"voice_text: {voice_text}")
                for vcmd in voice_commands:
                    if voice_text in voice_commands[vcmd][0]:
                        print(f"voice control match: {vcmd}")
                        current_voice_cmd = vcmd
                        voice_max_time =  voice_commands[vcmd][1]
                        break
                else:
                    print(f"voice control without match")

#. In ``remote_handler()`` function, the car moves according to the commands.

    .. code-block:: python

        def remote_handler():
            global current_voice_cmd, voice_start_time, voice_max_time
            ''' Voice Control '''
            if current_voice_cmd != None :

                if voice_max_time != 0:
                    if voice_start_time == 0:
                        voice_start_time = time.time()
                    if ((time.time() - voice_start_time) < voice_max_time):
                        if current_voice_cmd == "forward":
                            car.move("forward", VOICE_CONTROL_POWER)
                        elif current_voice_cmd == "backward":
                            car.move("backward", VOICE_CONTROL_POWER)
                        elif current_voice_cmd == "right":
                            car.move("right", VOICE_CONTROL_POWER)
                        elif current_voice_cmd == "left":
                            car.move("left", VOICE_CONTROL_POWER)
                        elif current_voice_cmd == "stop":
                            car.move("stop")
                    else:
                        current_voice_cmd = None
                        voice_start_time = 0
                        voice_max_time = 0
            else:
                car.move("stop")
