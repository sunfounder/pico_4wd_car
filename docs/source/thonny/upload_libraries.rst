
.. _upload_libraries_py:

3. Upload the Libraries to Pico (Optional)
===============================================

.. warning::
    Since we have already installed the MicroPython firmware and related libraries for the Raspberry Pi Pico at the factory. So this step and the next step can be skipped. But it is okay to follow the process if you want to.

Before using Pico-4wd Car, you need to upload its related libraries in Raspberry Pi Pico.


#. Download the relevant code from the link below.


   * :download:`SunFounder Pico-4wd Car V2.0 Code <https://github.com/sunfounder/pico_4wd_car/archive/refs/heads/v2.0.zip>`


#. Open Thonny IDE and plug the Pico into your computer with a micro USB cable and click on the "MicroPython (Raspberry Pi Pico).COMXX" interpreter in the bottom right corner.

    .. image:: img/sec_inter.png

#. In the top navigation bar, click **View** -> **Files**.

    .. image:: img/th_files.png

#. Switch the path to the folder where you downloaded the `code package <https://github.com/sunfounder/pico_4wd_car/archive/refs/heads/v2.0.zip>`_ before, and then go to the ``pico_4wd_car-v2.0/libs`` folder.

    .. image:: img/th_path.png

#. Select these 3 files, right-click and click **Upload to**, it will take a while to upload.

    .. image:: img/th_upload.png

#. Now you will see the files you just uploaded inside your drive ``Raspberry Pi Pico``.

    .. image:: img/th_pico_lib.png