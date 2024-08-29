# cutdetective
CutDetective is a Python script designed for Nuke that automates the detection of scene cuts in video files. It utilizes the PySceneDetect library to analyze video content and create corresponding FrameRange nodes within Nuke. This tool streamlines the process of breaking down footage into individual shots, allowing for efficient scene management and easy adjustments directly in your Nuke project.

## Installation Instructions for CutDetective Script

CutDetective relies on the PySceneDetect library for scene detection. You need to install it using pip:
**pip install scenedetect**

Place the cutdetective.py script in your .nuke directory or any directory of your choice.
To ensure the script loads automatically when you start Nuke, add the following line to your **.nuke/menu.py file**:
**nuke.pluginAddPath('path_to_cutdetective_directory')**
Replace path_to_cutdetective_directory with the actual path where cutdetective.py is located.

In Nuke, select a Read node that contains your video file.
Run the script through the Nuke interface, and it will prompt you to set the sensitivity for scene detection.

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
