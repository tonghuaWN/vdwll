"""
This file provides functionality of remotely controlling the content on the wall
by command line.
"""

import argparse


import Pyro4

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--func_name", type=str, required=True, help="name of the funtion to be run")
ap.add_argument("-n", "--name", type=str, required=True, help="the name of the widget")
ap.add_argument("-x", "--xpos", type=int, help="x coordinate of the new position")
ap.add_argument("-y", "--ypos", type=int, help="y coordinate of the new position")
ap.add_argument("-w", "--width", type=int, help="new width of the widget")
ap.add_argument("-ht", "--height", type=int, help="new height of the widget")
ap.add_argument("-u", "--uri", type=str, help="uri of the source")
ap.add_argument("-s", "--screen", type=str, required=True, help="IP address of the screen")
ap.add_argument("-cl", "--crop_left", type=int, help="Crop left as pixel")
ap.add_argument("-cr", "--crop_right", type=int, help="Crop right as pixel")
ap.add_argument("-ct", "--crop_top", type=int, help="Crop top as pixel")
ap.add_argument("-cb", "--crop_bottom", type=int, help="Crop bottom as pixel")


args = vars(ap.parse_args())


function_name = args["func_name"]
screen_ip = args["screen"]
screen = Pyro4.Proxy("PYRONAME:{}".format(screen_ip))  # bu komutun çalışacağı ekranı temsil ediyor.


def move_to(args):
    """
    python remote_machine_client.py -n"local video" -f="move_to" -s=192.168.1.35 -x=600 -y=400
    :param args:
    :return:
    """
    name = args["name"]
    xpos = args["xpos"]
    ypos = args["ypos"]
    screen.move_widget(name=name, xpos=xpos, ypos=ypos)


def resize(args):
    """
    python remote_machine_client.py -n"local video" -f="resize" -s=192.168.1.35 -w=600 -ht=400
    :param args:
    :return:
    """
    name = args["name"]
    width = args["width"]
    height = args["height"]
    screen.resize(name=name, width=width, height=height)


def remove(args):
    """
    sample usage:
    python remote_machine_client.py -n"local video" -f="remove" -s=192.168.1.35
    :param args:
    :return:
    """
    name = args["name"]
    screen.remove_widget(name=name)


def add_source(args):
    """
    sample usages:

    python remote_machine_client.py -f="add_source" \
    -n="rtsp source" -u=rtsp://10.0.0.143/media/video1 \
    -x=640 -y=0 -w=1280 -ht=720 -s=10.0.0.30


    python remote_machine_client.py -n"local video" \
    -u="file:///home/kemal/Developer/vdwll/media/brbad.mp4" \
    -x=100 -y=100 -w=1000 -ht=400 -f="add_source" \
    -s=192.168.1.35

    python remote_machine_client.py -n"local video" \
    -u="https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm" \
    -x=100 -y=100 -w=800 -ht=400 -f="add_source" \
    -s=192.168.1.35

    python remote_machine_client.py -n"local video" \
    -u="rtsp://10.0.0.143/media/video1" \
    -x=100 -y=100 -w=800 -ht=400 -f="add_source" \
    -s=10.0.0.27

    rtsp://78.188.204.20/media/video1
    rtsp://10.0.0.143/media/video1

    :param args:
    :return:
    """
    name = args["name"]
    uri = args["uri"]
    xpos = args["xpos"]
    ypos = args["ypos"]
    width = args["width"]
    height = args["height"]
    screen.add_source(name=name, uri=uri, xpos=xpos, ypos=ypos, width=width, height=height)


def change_mod_queue(args):
    """
    sample usage:
    python remote_machine_client.py -n"local video" -f="change_mod_queue" -s=10.0.0.27 \
    -w=1920 -ht=1080 -ct=0 -cr=300 -cl=300 -cb=0
    :param args:
    :return:
    """
    name = args["name"]
    width = args["width"]
    height = args["height"]
    crop_left = args["crop_left"]
    crop_right = args["crop_right"]
    crop_top = args["crop_top"]
    crop_bottom = args["crop_bottom"]

    print("crop_left", crop_left,
          "crop_right", crop_right,
          "crop_top", crop_top,
          "crop_bottom", crop_bottom)

    screen.change_mod_queue(name=name,
                            width=width,
                            height=height,
                            crop_left=crop_left,
                            crop_right=crop_right,
                            crop_top=crop_top,
                            crop_bottom=crop_bottom
                            )


locals()[function_name](args)

print("done!")
