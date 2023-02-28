# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import sphinx_rtd_theme
import time

project = 'SunFounder pico_4wd_car'
copyright = f'{time.localtime().tm_year}, SunFounder'
author = 'www.sunfounder.com'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autosectionlabel'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


# SunFounder logo

html_js_files = [
    'https://ezblock.cc/readDocFile/custom.js',
]
html_css_files = [
    'https://ezblock.cc/readDocFile/custom.css',
]

#### RTD+

#html_js_files = [
#    'https://ezblock.cc/readDocFile/custom.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/ace.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/ext-language_tools.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/theme-chrome.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/mode-python.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/mode-sh.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/monokai.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/xterm.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/FitAddon.js',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/js/readTheDocIndex.js',

#]
#html_css_files = [
#    'https://ezblock.cc/readDocFile/custom.css',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/css/index.css',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/css/xterm.css',
#]



# Multi-language

language = 'en' # Before running make html, set the language.
locale_dirs = ['locale/'] # .po files for other languages are placed in the locale/ folder.

gettext_compact = False # Support for generating the contents of the folders inside source/ into other languages.



# open link in a new window

rst_epilog = """

.. |link_ws2812b_datasheet| raw:: html

    <a href="https://www.digikey.com/en/datasheets/parallaxinc/parallax-inc-28085-ws2812b-rgb-led-datasheet" target="_blank">WS2812B Datasheet</a>

.. |link_tcrt5000_datasheet| raw:: html

    <a href="https://datasheetspdf.com/pdf-file/377371/VishayTelefunken/TCRT5000/1" target="_blank">TCRT5000</a>

.. |link_sn74lvc2g14dbvr_datasheet| raw:: html

    <a href="https://pdf1.alldatasheet.com/datasheet-pdf/view/82961/TI/SN74LVC2G14DBVR.html" target="_blank">datasheet</a>

.. |link_pwm| raw:: html

    <a href="https://en.wikipedia.org/wiki/Pulse-width_modulation" target="_blank">Pulse-width Modulation</a>

.. |link_class| raw:: html

    <a href="https://en.wikipedia.org/wiki/Class_(computer_programming)" target="_blank">Class</a>

.. |link_pio| raw:: html

    <a href="https://hackspace.raspberrypi.com/articles/what-is-programmable-i-o-on-raspberry-pi-pico" target="_blank">Programmable IO(PIO)</a>

.. |link_pio_micropython| raw:: html

    <a href="https://docs.micropython.org/en/latest/rp2/tutorial/pio.html" target="_blank">Programmable IO - MicroPython</a>





.. |link_api_car| raw:: html

    <a href="https://github.com/sunfounder/pico_4wd_car/blob/main/api_reference_pico_4wd.md" target="_blank">API</a>

.. |link_realpython| raw:: html

    <a href="https://realpython.com/micropython/" target="_blank">realpython</a>

.. |link_micropython_pi| raw:: html

    <a href="https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython" target="_blank">method</a>

.. |link_thonny| raw:: html

    <a href="https://thonny.org/" target="_blank">Thonny</a>

.. |link_websocket| raw:: html

    <a href="https://en.wikipedia.org/wiki/WebSocket" target="_blank">WebSocket - Wikipedia</a>

.. |link_pico_4wd_github| raw:: html

    <a href="https://github.com/sunfounder/pico_4wd_car" target="_blank">Pico-4wd Car - GitHub</a>

.. |link_sunfounder_controller| raw:: html

    <a href="https://docs.sunfounder.com/projects/sf-controller/en/latest/" target="_blank">SunFounder Control</a>

.. |link_micropython| raw:: html

    <a href="https://en.wikipedia.org/wiki/MicroPython" target="_blank">MicroPython - Wikipedia</a>
    


"""

# pictures

rst_epilog += """

.. |app_save| image:: /img/app/app_save.jpg
    :width: 20

.. |app_run| image:: /img/app/app_run.png
    :width: 20

.. |app_connect| image:: /img/app/app_connect.jpg
    :width: 20

.. |app_speech_i| image:: /img/app/app_speech_i.png
    :width: 40

.. |thonny_run| image:: /thonny/img/thonny_run.png
    :width: 20

.. |thonny_stop| image:: /thonny/img/thonny_stop.png
    :width: 20

.. |app_edit| image:: /img/app/app_edit.jpg
    :width: 20


"""