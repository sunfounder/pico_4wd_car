Test Your Module
==================================

.. note::
    在进行该环节之前，请确保你已经完成了 :ref:`Setup Your Pico` 中的设置。

在 **test** 文件夹下找到 ``test.py`` ，这是一个专门用于测试Pico-4wd能否正常工作的文件，please open it with Thonny.


Servo Zeroing During Assembly
--------------------------------------

这一部分适用于装配步骤中的 **Assemble Ultrasonic Module** （准确的说是其中的step2）。

.. note::
    下方代码被简写，请打开``test.py``文件使用该代码。


.. code-block::
    :emphasize-lines: 10,36

    import pico_4wd as car
    import time

    def test_motor():
        #...

    def test_sonar():
        #...

    def test_servo():
        for angle in range(0, 90):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.005)
        for angle in range(90, -90, -1):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.005)
        for angle in range(-90, 0):
            print("angle:%s "%angle)
            car.servo.set_angle(angle)
            time.sleep(0.005)

    def test_light():
        #...

    def test_grayscale():
        #...

    def test_speed():
        #...

    try:
        # test_motor()
        # test_sonar()
        test_servo()
        # test_light()
        # test_grayscale()
        # test_speed()
    finally:
        car.move("stop")
        car.set_light_off()

这个文件中有6个test函数，我们注释了其中五个，执行了 ``test_servo()`` ，它的作用是让舵机轴来回偏转一次，最终定格在 0° 。
你可以在执行该程序之前装入一个闲置的Servo Arm以便于更好的观察程序是否执行顺利。舵机轴角度归零后，则可以继续接下来的安装步骤了。


Test Modules During Play
------------------------------

这一部分适用于完成组装后，对Pico-4wd进行最终调试或维护的环节。

.. note::
    下方代码被简写，请打开``test.py``文件使用该代码）。


.. code-block::
    :emphasize-lines: 23,24,25,26,27,28

    import pico_4wd as car
    import time

    def test_motor():
        #...

    def test_sonar():
        #...

    def test_servo():
        #...

    def test_light():
        #...

    def test_grayscale():
        #...

    def test_speed():
        #...

    try:
        # test_motor()
        # test_sonar()
        test_servo()
        # test_light()
        # test_grayscale()
        # test_speed()
    finally:
        car.move("stop")
        car.set_light_off()

具体的使用步骤如下：

1. 将 ``test_motor()`` , ``test_sonar()`` , ``test_servo()`` , ``test_light()`` , ``test_grayscale()`` , ``test_speed()`` 这六行全部注释（To know about :ref:`Comments` here if you need）. 

#. 将你需要测试的模块所对应的语句取消注释。如需测试电机，则uncomment ``test_motor()`` 。同一时间只能进行一个测试项。
#. 运行程序。
#. 这些函数中的一些含有 ``while True`` 循环，需要手动stop them。


每一个测试函数被调用时将会发生以下现象：

**test_motor()**

该函数会让Pico-4wd执行前进、后退、左转、右转、停止五个动作。

**test_sonar()**

该函数会让超声波模块检测其前方的障碍物，并打印障碍物的距离。

**test_light()**

该函数会让24个LED（3个RGB board上所有的）依次发出红光、依次发出绿光、依次发出蓝光、依次发出白光。

**test_grayscale()**

该函数会打印grayscale module三个探测头的值。使用时你应当将小车放在桌面， the probe should be about 5 mm from the ground.  Normally, it will detect a value above ``1100`` on white ground. On black ground, it will detect values below ``900``. On a cliff, it will detect a value below ``110`` . (If the reading is ``0`` , it means that the probe does not detect the ground.)

**test_speed()**

该函数会让Pico-4wd变速前进，并将马达功率（百分比）及行驶速度(cm/s)打印出来。使用时你应当悬空小车，让马达转动不被阻碍。

.. note::
    Thonny IDE中含有折线图工具，请在导航栏中点击 View > Plotter 打开它，以助于你查看打印值的变化情况。

