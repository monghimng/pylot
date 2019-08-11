import pylot

FRONT = 'front'
RIGHT = 'right'
BACK = 'back'
LEFT = 'left'

FRONT_SEGMENTED= 'front_segmented'
RIGHT_SEGMENTED= 'right_segmented'
BACK_SEGMENTED= 'back_segmented'
LEFT_SEGMENTED= 'left_segmented'

FRONT_DEPTH= 'front_depth'
RIGHT_DEPTH= 'right_depth'
BACK_DEPTH= 'back_depth'
LEFT_DEPTH= 'left_depth'
TOP_DOWN_SEGMENTED = 'top_down_segmented'

OVERHEAD_LOCATION = pylot.simulation.utils.Location(0, 0, 2)
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080

RGB_CAMERA_TYPE = 'sensor.camera.rgb'
SEGMENTED_CAMERA_TYPE = 'sensor.camera.semantic_segmentation'
DEPTH_CAMERA_TYPE = 'sensor.camera.depth'

CAMERA_NAME_TO_CAMERA_SETUP = {

    TOP_DOWN_SEGMENTED: pylot.simulation.utils.CameraSetup(
        TOP_DOWN_SEGMENTED,
        SEGMENTED_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            pylot.simulation.utils.Location(0, 0, 20),  # x meters above the vehicle center
            pylot.simulation.utils.Rotation(-90, 0, 0)  # face down
        )
    ),

    FRONT: pylot.simulation.utils.CameraSetup(
        FRONT,
        RGB_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 0, 0) # face forward
        )
    ),

    RIGHT: pylot.simulation.utils.CameraSetup(
        RIGHT,
        RGB_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 90, 0) # face forward
        )
    ),

    BACK: pylot.simulation.utils.CameraSetup(
        BACK,
        RGB_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 180, 0) # face forward
        )
    ),

    LEFT: pylot.simulation.utils.CameraSetup(
        LEFT,
        RGB_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 270, 0) # face forward
        )
    ),

    FRONT_SEGMENTED: pylot.simulation.utils.CameraSetup(
        FRONT_SEGMENTED,
        SEGMENTED_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 0, 0) # face forward
        )
    ),

    RIGHT_SEGMENTED: pylot.simulation.utils.CameraSetup(
        RIGHT_SEGMENTED,
        SEGMENTED_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 90, 0) # face forward
        )
    ),

    BACK_SEGMENTED: pylot.simulation.utils.CameraSetup(
        BACK_SEGMENTED,
        SEGMENTED_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 180, 0) # face forward
        )
    ),

    LEFT_SEGMENTED: pylot.simulation.utils.CameraSetup(
        LEFT_SEGMENTED,
        SEGMENTED_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 270, 0) # face forward
        )
    ),

    FRONT_DEPTH: pylot.simulation.utils.CameraSetup(
        FRONT_DEPTH,
        DEPTH_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 0, 0) # face forward
        )
    ),

    RIGHT_DEPTH: pylot.simulation.utils.CameraSetup(
        RIGHT_DEPTH,
        DEPTH_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 90, 0) # face forward
        )
    ),

    BACK_DEPTH: pylot.simulation.utils.CameraSetup(
        BACK_DEPTH,
        DEPTH_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 180, 0) # face forward
        )
    ),

    LEFT_DEPTH: pylot.simulation.utils.CameraSetup(
        LEFT_DEPTH,
        DEPTH_CAMERA_TYPE,
        DEFAULT_WIDTH,
        DEFAULT_HEIGHT,
        pylot.simulation.utils.Transform(
            OVERHEAD_LOCATION,
            pylot.simulation.utils.Rotation(0, 270, 0) # face forward
        )
    ),
}

CAMERA_NAMES = CAMERA_NAME_TO_CAMERA_SETUP.keys()
CAMERA_SETUPS = CAMERA_NAME_TO_CAMERA_SETUP.values()

CAMERA_PRESET = {
    '4side': [FRONT, RIGHT, BACK, LEFT],
    '4side_segmented': [FRONT_SEGMENTED, RIGHT_SEGMENTED, BACK_SEGMENTED, LEFT_SEGMENTED],
    '4side_depth': [FRONT_DEPTH, RIGHT_DEPTH, BACK_DEPTH, LEFT_DEPTH],
}

def get_camera_setup_by_name(name):
    assert name in  CAMERA_NAMES, 'camera named {} is not one of the predefined camera in the list {}'.format(name, CAMERA_NAMES)
    return CAMERA_NAME_TO_CAMERA_SETUP[name]

def get_camera_setups_by_names(names):

    setups = []
    for name in names:

        # if the name is one of the predefined set of cameras
        if name in CAMERA_PRESET.keys():
            for name_in_set in CAMERA_PRESET[name]:
                setup = get_camera_setup_by_name(name_in_set)
                setups.append(setup)
        else:
            setup = get_camera_setup_by_name(name)
            setups.append(setup)

    return setups
