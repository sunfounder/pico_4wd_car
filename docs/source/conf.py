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

project = 'SunFounder pico_4wd_car'
copyright = '2021, SunFounder'
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
    'https://ezblock.cc/readDocFile/topHead.js',
]
html_css_files = [
    'https://ezblock.cc/readDocFile/topHead.css',
]

#### RTD+

#html_js_files = [
#    'https://ezblock.cc/readDocFile/topHead.js',
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
#    'https://ezblock.cc/readDocFile/topHead.css',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/css/index.css',
#    'https://ezblock.cc/readDocFile/readTheDoc/src/css/xterm.css',
#]



# Multi-language

language = 'en' # Before running make html, set the language.
locale_dirs = ['locale/'] # .po files for other languages are placed in the locale/ folder.

gettext_compact = False # Support for generating the contents of the folders inside source/ into other languages.


# pico micropython start
rst_epilog = """
.. |mps_bootsel_onboard| image:: /img/micropython_start/bootsel_onboard.png
.. |mps_th_files| image:: /img/micropython_start/th_files .png
.. |mps_th_path| image:: /img/micropython_start/th_path.png
.. |mps_th_pico| image:: /img/micropython_start/th_pico.png
.. |mps_th_upload| image:: /img/micropython_start/th_upload.png
.. |mps_th_done| image:: /img/micropython_start/th_done.png
.. |mps_interpreter| image:: /img/micropython_start/interpreter.png
.. |mps_index_htm| image:: /img/micropython_start/index_htm.png
.. |mps_welcome_pico| image:: /img/micropython_start/welcome_pico.png
.. |mps_download_uf2| image:: /img/micropython_start/download_uf2.png
.. |mps_move_uf2| image:: /img/micropython_start/move_uf2.png
.. |mps_download_thonny| image:: /img/micropython_start/download_thonny.png
.. |mps_thonny_ide.jpg| image:: /img/micropython_start/thonny_ide.jpg
.. |mps_hello_shell| image:: /img/micropython_start/hello_shell.png
.. |mps_hello_world_script| image:: /img/micropython_start/hello_world_script.png
.. |mps_where_save| image:: /img/micropython_start/where_save.png
.. |mps_hello_world_save| image:: /img/micropython_start/hello_world_save.png
.. |mps_open_code| image:: /img/micropython_start/open_code.png
.. |mps_sec_inter| image:: /img/micropython_start/sec_inter.png
.. |mps_run_it| image:: /img/micropython_start/run_it.png
.. |mps_stop_it| image:: /img/micropython_start/stop_it.png
.. |mps_save_as| image:: /img/micropython_start/save_as.png
.. |mps_sec_pico| image:: /img/micropython_start/sec_pico.png
.. |mps_sec_name| image:: /img/micropython_start/sec_name.png
.. |mps_new_file| image:: /img/micropython_start/new_file.png
.. |mps_copy_file| image:: /img/micropython_start/copy_file.png

"""


# sunfounder controller
rst_epilog += """
.. |sc_app_install| image:: /img/esp8266/sc_app_install.png
.. |sc_upload_ws| image:: /img/esp8266/upload_ws.png
.. |sc_run_test| image:: /img/esp8266/run_test.png
.. |sc_app_create_controller| image:: /img/esp8266/sc_app_create_controller.jpg
.. |sc_app_interface| image:: /img/esp8266/sc_app_interface.jpg
.. |sc_sec_radar| image:: /img/esp8266/sec_radar.jpg
.. |sc_sec_slide| image:: /img/esp8266/sec_slide.jpg
.. |sc_run_save| image:: /img/esp8266/run_save.jpg
.. |sc_app_actuator| image:: /img/esp8266/sc_app_actuator.jpg
.. |flowchart_app_control| image:: /img/esp8266/flowchart_app_control.png
.. |sc_app_widget_act| image:: /img/esp8266/sc_app_act.png
.. |sc_app_widget_dis| image:: /img/esp8266/sc_app_dis.png
.. |sc_app_connect_anyway| image:: /img/esp8266/connect_anyway.png
.. |sc_app_click-disconnect| image:: /img/esp8266/click-disconnect.jpg
.. |sc_app_auto_connect| image:: /img/esp8266/auto_connect.jpg
.. |sc_app_control_widget| image:: /img/esp8266/control_widget.png
.. |sc_app_show_widget| image:: /img/esp8266/show_widget.png
.. |sc_ws_test_data| image:: /img/esp8266/ws_test_data.png
.. |sc_save_main| image:: /img/esp8266/save_main.png
.. |sc_app_control_example| image:: /img/esp8266/app_control_example.jpg
.. |sc_seach_wifi| image:: /img/esp8266/seach_wifi.jpg

"""


# sunfounder controller
rst_epilog += """
.. |example_avoid| image:: /img/example_avoid.png
.. |example_cliff| image:: /img/example_cliff.png
.. |example_follow| image:: /img/example_follow.png
.. |example_line| image:: /img/example_line.png

"""