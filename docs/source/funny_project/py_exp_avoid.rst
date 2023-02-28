4. Obstacle Avoid
========================

.. image:: img/example_avoid.png

Let Pico-4wd do a challenging task: automatically avoid obstacles! 
When an obstacle is detected, instead of simply backing up, 
the sonar scans the surrounding area and finds the widest way 
to move forward.


完整代码请看 ``examples`` 目录下的 ``project_4_avoid.py`` 文件。


**How to do?**

这个项目相当于 ``py_exp_follow`` 的升级版，如先完成那个篇章，你会对该项目有更清晰的了解。
两者的区别在于另一者是寻找障碍所在的方向，而这里需要的是寻找没有障碍的方向。

1. 小车对环境进行扫描，在左中右三个方向中找出最宽的车道。如果没有可通行的路，则返回左。

    .. code-block:: python

        import sonar as sonar
        import motors as car
        import time

        def get_dir(data,split_str='0'):

            # get scan status of 0, 1
            data = [str(i) for i in data]
            data = "".join(data)

            # Split 0, leaves the free path
            paths = data.split(split_str)

            # Find the max path
            max_paths=max(paths)

            # If no wide enough path
            if len(max_paths)<4:
                return "left"

            # Calculate the direction of the widest one
            position = data.index(max_paths) # find the widest path position
            position += (len(max_paths)-1)/2 # find the middle of the widest path

            # Divide the scanning area into three pieces and mark the widest one
            if position < len(data) / 3: 
                return "left"
            elif position > 2 * len(data) / 3:
                return "right"
            else:
                return "forward"

        try:
            sonar.set_sonar_scan_config(scan_range=60, step=10)
            sonar.set_sonar_reference(30)
            while True:
                _, _, sonar_data = sonar.sonar_scan()
                # sonar_data: 0 is block, 1 is pass
                time.sleep(0.04)

                # If sonar data return a int, means scan not finished, and the int is current angle status
                if isinstance(sonar_data, int): 
                    continue # only list can go on

                direction = get_dir(sonar_data,split_str='0')
                print("The Car Should Go: ", direction)
                
        finally:
            pass


2. 让小车转向最宽的道路，然后前进。在小车往右旋转时，它会同时看向（sonar朝向）左侧，直到检测不到障碍物了，才完成这次旋转。往左转时同理。


    .. code-block:: python
        :emphasize-lines: 33,35,36,37,38,,39,40,41,42,43,45,46,47,48,49,50,51,52,53,71

        import sonar as sonar
        import motors as car
        import time

        def get_dir(data,split_str='0'):

            # get scan status of 0, 1
            data = [str(i) for i in data]
            data = "".join(data)

            # Split 0, leaves the free path
            paths = data.split(split_str)

            # Find the max path
            max_paths=max(paths)

            # If no wide enough path
            if len(max_paths)<4:
                return "left"

            # Calculate the direction of the widest one
            position = data.index(max_paths) # find the widest path position
            position += (len(max_paths)-1)/2 # find the middle of the widest path

            # Divide the scanning area into three pieces and mark the widest one
            if position < len(data) / 3: 
                return "left"
            elif position > 2 * len(data) / 3:
                return "right"
            else:
                return "forward"

        def running(direction,power):
            if direction is "left":
                sonar.get_distance_at(20) # face right
                time.sleep(0.2)
                car.move("left", power*2)
                while True:
                    distance = sonar.get_distance_at(20) # face right
                    status = sonar.get_sonar_status(distance)
                    if status is 1: # right position is pass
                        break
                car.move("stop")
            elif direction is "right":
                sonar.get_distance_at(-20) # face left
                time.sleep(0.2)
                car.move("right", power*2)
                while True:
                    distance = sonar.get_distance_at(-20) # face left
                    status = sonar.get_sonar_status(distance)
                    if status is 1: # left position is pass
                        break
                car.move("stop")
            else:
                # pass
                car.move("forward",power)

        try:
            MOTOR_POWER = 30
            sonar.set_sonar_scan_config(scan_range=60, step=10)
            sonar.set_sonar_reference(30)
            while True:
                _, _, sonar_data = sonar.sonar_scan()
                # sonar_data: 0 is block, 1 is pass
                time.sleep(0.04)

                # If sonar data return a int, means scan not finished, and the int is current angle status
                if isinstance(sonar_data, int): 
                    continue # only list can go on
                direction = get_dir(sonar_data,split_str='0')
                running(direction, MOTOR_POWER)
                
        finally:
            car.move("stop")

3. 小车在前进时只需要检测前方是否有障碍，而在检测到障碍物时，它应当停下并寻找新的道路。这也意味着雷达的搜索范围要从前方60°变成180°。

.. code-block:: python
    :emphasize-lines: 60,61,62,64,73,74,75,76,80,81

    import sonar as sonar
    import motors as car
    import time

    def get_dir(data,split_str='0'):

        # get scan status of 0, 1
        data = [str(i) for i in data]
        data = "".join(data)

        # Split 0, leaves the free path
        paths = data.split(split_str)

        # Find the max path
        max_paths=max(paths)

        # If no wide enough path
        if len(max_paths)<4:
            return "left"

        # Calculate the direction of the widest one
        position = data.index(max_paths) # find the widest path position
        position += (len(max_paths)-1)/2 # find the middle of the widest path

        # Divide the scanning area into three pieces and mark the widest one
        if position < len(data) / 3: 
            return "left"
        elif position > 2 * len(data) / 3:
            return "right"
        else:
            return "forward"

    def running(direction,power):
        if direction is "left":
            sonar.get_distance_at(20) # face right
            time.sleep(0.2)
            car.move("left", power*2)
            while True:
                distance = sonar.get_distance_at(20) # face right
                status = sonar.get_sonar_status(distance)
                if status is 1: # right position is pass
                    break
            car.move("stop")
        elif direction is "right":
            sonar.get_distance_at(-20) # face left
            time.sleep(0.2)
            car.move("right", power*2)
            while True:
                distance = sonar.get_distance_at(-20) # face left
                status = sonar.get_sonar_status(distance)
                if status is 1: # left position is pass
                    break
            car.move("stop")
        else:
            # pass
            car.move("forward",power)

    try:
        MOTOR_POWER = 30
        SCAN_RANGE_PASS = 60
        SCAN_RANGE_BLOCK = 180
        SCAN_STEP = 10
        status = "pass"
        sonar.set_sonar_scan_config(scan_range=SCAN_RANGE_PASS, step=SCAN_STEP)
        sonar.set_sonar_reference(30)
        while True:
            _, _, sonar_data = sonar.sonar_scan()
            # sonar_data: 0 is block, 1 is pass
            time.sleep(0.04)

            # If sonar data return a int, means scan not finished, and the int is current angle status
            if isinstance(sonar_data, int): 
                if sonar_data is 0 and status is "pass": #If it finds an obstacle
                    status = "block"
                    car.move("stop") 
                    sonar.set_sonar_scan_config(SCAN_RANGE_BLOCK) # change scan range to 180 and re-scan
                continue # only list can go on
            direction = get_dir(sonar_data,split_str='0')
            running(direction, MOTOR_POWER)
            status = "pass" # find a passable way
            sonar.set_sonar_scan_config(SCAN_RANGE_PASS) # change scan range to 60 for go forward
            
    finally:
        car.move("stop")
