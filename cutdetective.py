# Natalia Raz
# Based on https://github.com/Breakthrough/PySceneDetect

import nuke
import time
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

def detect_scenes(video_path, threshold):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    video_manager.set_downscale_factor()
    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    scene_list = scene_manager.get_scene_list()

    video_manager.release()

    return scene_list

def frames_to_timecode(frame, fps):
    # Converts frame number to timecode in the format HH:MM:SS:FF
    seconds = frame / fps
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    frames = int((frame % fps))
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

def update_frame_range_labels(shot_nodes, show_timecode=True):
    fps = nuke.root()['fps'].value()  # Get the FPS value from the project settings

    for node in shot_nodes:
        # Get the values of the first and last frame
        first_frame = int(node['first_frame'].value())
        last_frame = int(node['last_frame'].value())

        # Convert frame numbers to timecodes
        first_timecode = frames_to_timecode(first_frame, fps)
        last_timecode = frames_to_timecode(last_frame, fps)

        # Determine the label format based on the show_timecode flag
        if show_timecode:
            label = f"{first_frame}-{last_frame}\n{first_timecode} - {last_timecode}"
        else:
            label = f"{first_frame}-{last_frame}"

        # Set the label on the node
        node['label'].setValue(label)

def run_scene_detection():
    selected_node = nuke.selectedNode()
    if selected_node.Class() == 'Read':
        video_path = selected_node['file'].value()
        if video_path:
            sensitivity = nuke.getInput("Enter sensitivity for scene detection (default is 30):", "30")
            if not sensitivity:
                nuke.message("Operation cancelled.")
                return
            try:
                sensitivity = float(sensitivity)
            except ValueError:
                nuke.message("Invalid sensitivity value.")
                return

            task = nuke.ProgressTask("Scene Detection")
            task.setMessage("Analyzing video...")

            try:
                start_time = time.time()

                scene_list = detect_scenes(video_path, threshold=sensitivity)
                task.setProgress(50)
                task.setMessage("Creating nodes...")

                dot_node = nuke.createNode('Dot')
                dot_node.setInput(0, selected_node)

                total_scenes = len(scene_list)
                shot_nodes = []

                for i, (start_time_scene, end_time_scene) in enumerate(scene_list):
                    if task.isCancelled():
                        nuke.executeInMainThread(nuke.message, args=("Scene detection cancelled",))
                        return

                    start_frame = int(start_time_scene.get_frames()) + 1
                    end_frame = int(end_time_scene.get_frames())

                    frame_range_node = nuke.createNode('FrameRange')
                    frame_range_node['first_frame'].setValue(start_frame)
                    frame_range_node['last_frame'].setValue(end_frame)
                    frame_range_node.setName(f'Shot_{i+1}')
                    frame_range_node.setInput(0, dot_node)

                    if not frame_range_node.knob('original_first_frame'):
                        original_first_frame = nuke.Int_Knob('original_first_frame', 'Original First Frame')
                        frame_range_node.addKnob(original_first_frame)
                        frame_range_node['original_first_frame'].setValue(start_frame)

                    # Set the label with the frame range and timecode
                    update_frame_range_labels([frame_range_node])

                    shot_nodes.append(frame_range_node)
                    task.setMessage(f"Creating nodes... ({i+1}/{total_scenes}) - Time left: {int((time.time() - start_time) / (i + 1) * total_scenes - (time.time() - start_time))}s")
                    task.setProgress(int((i + 1) / total_scenes * 50) + 50)
                    time.sleep(0.1)

                # Update labels for all shots
                update_frame_range_labels(shot_nodes)

                nuke.executeInMainThread(nuke.message, args=("Scene detection completed",))

                # Create a node with a button for shot recalculation
                add_update_button_node(selected_node)
            except Exception as e:
                nuke.executeInMainThread(nuke.message, args=(str(e),))
            finally:
                task.setProgress(100)
    else:
        nuke.message("Please select a Read node with a video file.")

def update_shot_frames(shot_nodes, show_timecode=True):
    def find_first_frame():
        shot1 = shot_nodes[0]
        if not shot1['disable'].value():
            return shot1['original_first_frame'].value()
        else:
            return shot1['original_first_frame'].value()

    previous_frame = None

    for node in shot_nodes:
        if node['disable'].value():
            continue

        if previous_frame is None:
            first_frame = find_first_frame()
        else:
            first_frame = previous_frame + 1

        node['first_frame'].setValue(first_frame)
        previous_frame = node['last_frame'].value()

    # Update labels for all shots after recalculation
    update_frame_range_labels(shot_nodes, show_timecode)

def update_shots_after_changes():
    shot_nodes = [node for node in nuke.allNodes() if node.Class() == 'FrameRange']
    shot_nodes.sort(key=lambda node: int(node.name().split('_')[1]))

    # Get the show_timecode value from the checkbox
    update_node = nuke.toNode("Update_Shots_Node")
    show_timecode = update_node['show_timecode'].value()

    update_shot_frames(shot_nodes, show_timecode)

def knob_changed():
    # This function will be called whenever any knob is changed
    knob = nuke.thisKnob()
    node = nuke.thisNode()

    # Check if the changed knob is the show_timecode knob
    if knob.name() == "show_timecode":
        update_shots_after_changes()

def add_update_button_node(selected_node):
    # Create a NoOp node with a button without connecting to other nodes
    update_node = nuke.nodes.NoOp()
    update_node.setName("Update_Shots_Node")

    # Create a button and add it to the node
    update_button = nuke.PyScript_Knob('update_button', 'Update_FrameRange')
    update_button.setCommand('update_shots_after_changes()')
    update_node.addKnob(update_button)

    # Create a checkbox to toggle timecode visibility
    show_timecode_knob = nuke.Boolean_Knob('show_timecode', 'Show Timecode')
    show_timecode_knob.setValue(True)  # Default to show timecode
    update_node.addKnob(show_timecode_knob)

    # Set the node's color to green
    update_node['tile_color'].setValue(0x9F00FF)

    # Place it next to the `Read` node
    update_node['xpos'].setValue(selected_node['xpos'].value() + 100)  # Shift by X
    update_node['ypos'].setValue(selected_node['ypos'].value())  # Align by Y

# Run the main function
run_scene_detection()
