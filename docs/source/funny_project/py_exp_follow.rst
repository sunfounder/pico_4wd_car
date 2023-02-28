.. _py_exp_follow:

3. Follow
====================

在这个项目中。Pico-4wd会跟着前方的物体行动，比如你把手放在它的面前，它会往你的手冲过去。
而且它还会发挥雷达扫描的优点，会判断你的手是位于它的左前方还是正前方，微调前进方向。




完整代码请看 ``examples`` 目录下的 ``project_3_follow.py`` 文件。


**How to do?**

1. 在这个项目中，我们用到了 motor， servo 和 ultrasonic。 这意味着我们需要使用 ``motors.py``, ``motor.py``, ``servo.py``, ``ultrasonic``, ``sonar`` 这几个库，请将它们从 ``libs`` 文件夹中上传到pico。 然后在项目中import它们。

    .. code-block:: python

        import sonar as sonar
        import motors as car
        import time

2. 让小车对前方进行扫描。


.. code-block:: python

    import sonar as sonar
    import motors as car
    import time

    try:
        sonar.set_sonar_scan_config(scan_range=90, step=10)
        while True:
            _,_,sonar_data = sonar.sonar_scan()
            # sonar_data: 0 is block, 1 is pass
            time.sleep(0.04)

            # If sonar data return a int, means scan not finished, and the int is current angle status
            if isinstance(sonar_data,int):
                continue # only list can go on

            print(sonar_data)

    finally:
        pass

3. 对扫描结果进行处理，找出障碍物(通常是你的手)的方向。把方向划分为左，中，右。如果没有障碍物，则返回stop。







.. code-block:: python
    :emphasize-lines: 5,49

    import sonar as sonar
    import motors as car
    import time

    def get_dir(data,split_str='0'):

        # get scan status of 0, 1
        data = [str(i) for i in data]
        data = "".join(data)
        print("Data: ",data)

        # Split 1, leaves the object path
        paths = data.split(split_str)
        print("Divide the Data: ", paths)

        # Find the max path
        max_paths=max(paths)
        print("Max Path: ",max_paths)

        # If no object
        if len(max_paths)<3:
            return "stop"

        # Calculate the direction of the biggest one
        position = data.index(max_paths) # find the biggest object position
        position += (len(max_paths)-1)/2 # find the middle of the biggest object
        print("Max Path's Direction: ",position)

        # Divide the scanning area into three pieces and mark the right one
        if position < len(data) / 3: 
            return "left"
        elif position > 2 * len(data) / 3:
            return "right"
        else:
            return "forward"


    try:
        sonar.set_sonar_scan_config(scan_range=90, step=10)
        while True:
            _,_,sonar_data = sonar.sonar_scan()
            # sonar_data: 0 is block, 1 is pass
            time.sleep(0.04)
            
            # If sonar data return a int, means scan not finished, and the int is current angle status
            if isinstance(sonar_data,int):
                continue # only list can go on

            direction = get_dir(sonar_data,split_str='1')
            print("The Car Should Go: ", direction)

    finally:
        pass


4. 让小车转向障碍物(你的手)，然后前进。

.. code-block:: python
    :emphasize-lines: 31,54

    import sonar as sonar
    import motors as car
    import time

    def get_dir(data,split_str='0'):

        # get scan status of 0, 1
        data = [str(i) for i in data]
        data = "".join(data)

        # Split 1, leaves the object path
        paths = data.split(split_str)
        max_paths=max(paths)

        # no object
        if len(max_paths)<3:
            return "stop"

        # Calculate the direction of the biggest one
        position = data.index(max_paths) # find the biggest object position
        position += (len(max_paths)-1)/2 # find the middle of the biggest object

        # Divide the scanning area into three pieces and mark the right one
        if position < len(data) / 3: 
            return "left"
        elif position > 2 * len(data) / 3:
            return "right"
        else:
            return "forward"

    def running(direction,power):
        if direction == "left":
            car.move("left", power)
        elif direction == "right":
            car.move("right", power)
        elif direction == "forward":
            car.move("forward", power)
        else:
            car.move("stop")

    try:
        MOTOR_POWER = 20
        sonar.set_sonar_scan_config(scan_range=90, step=10)
        while True:
            _,_,sonar_data = sonar.sonar_scan()
            # sonar_data: 0 is block, 1 is pass
            time.sleep(0.04)
            
            # If sonar data return a int, means scan not finished, and the int is current angle status
            if isinstance(sonar_data,int):
                continue # only list can go on

            direction = get_dir(sonar_data,split_str='1')
            running(direction,MOTOR_POWER)

    finally:
        car.move("stop")