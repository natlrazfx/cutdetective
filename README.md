# cutdetective
CutDetective is a Python script designed for Nuke that automates the detection of scene cuts in video files. It utilizes the PySceneDetect library to analyze video content and create corresponding FrameRange nodes within Nuke. This tool streamlines the process of breaking down footage into individual shots, allowing for efficient scene management and easy adjustments directly in your Nuke project.

## Installation Instructions for CutDetective Script

CutDetective relies on the PySceneDetect library for scene detection. You need to install it using pip:
**pip install --upgrade scenedetect[opencv]**

**it's recommended to familiarize yourself with the PySceneDetect library. This library provides detailed documentation on how scene detection works and the various parameters available for configuration. Understanding this will help you get the most out of the Cut Detective Studio script and optimize it for your specific workflow.
You can find more information and documentation for PySceneDetect here [PySceneDetect Documentation](https://www.scenedetect.com/download/)**

Place the cutdetective.py script in your .nuke directory or any directory of your choice.
You can run the script through the Script Editor, bind it to a hotkey, or (recommended) add it to your w_hotbox for quick access.

To run it from the Script Editor, remove the run_scene_detection() line from the script. Insert the following into your menu.py:
**import cutdetective
nuke.menu("Nuke").addCommand('Time/Cutdetective', 'cutdetective.run_scene_detection()')**

In Nuke, select a Read node that contains your video file.
It will prompt you to set the sensitivity for scene detection.

*Note: 
By default, it's set to 30, which usually works pretty well. If you want to experiment, you can adjust the value higher or lower. Increasing the sensitivity value detects more subtle changes and might result in more cuts, while lowering it could miss some scene changes.*

[![Watch the video](https://img.youtube.com/vi/CNX4QDJAd98/maxresdefault.jpg)](https://youtu.be/CNX4QDJAd98)

## Support and Feedback

If this script saved you some time or you just love what it does, please feel free to share your thoughts and consider supporting my work as I continue my journey

### 💖 GitHub Sponsors
[Become a Sponsor](https://github.com/sponsors/natlrazfx)
### ☕ Buy Me a Coffee
[Buy Me a Coffee](https://www.buymeacoffee.com/natlrazfx)
### 💸 PayPal
[PayPal Me](https://paypal.me/natlrazfx)
### 👾 ByBit
119114169


## Cheers :) 
