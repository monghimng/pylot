class CameraSetup:

    def __init__(self, rgb=[], segmented=[], depth=[], rgb_transform=[], segmented_transform=[], depth_transform=[]):
        self.rgb_camera_names = rgb
        self.segmented_camera_names = segmented
        self.depth_camera_names = depth

        self.rgb_camera_transform = rgb_transforms
        self.segmented_camera_transform = segmented_transforms
        self.depth_camera_transform = depth_transforms

def get_camera_setups(setup_config):

    setup = CameraSetup()

    if 'top_down_segmented' in setup_config:
        setup_top_down_segmented(setup)

    return setup

def setup_top_down_segmented(camera_setup):
    top_down_location = pylot.simulation.utils.Location(0, 0, 30)  # x meters above the vehicle center
    top_down_rotation = pylot.simulation.utils.Rotation(-90, 0, 0)  # face down
    top_down_transform = pylot.simulation.utils.Transform(top_down_location, top_down_rotation)
    camera_setup.segmented_camera_names.append('top_down_segmented')
    camera_setup.segmented_camera_transforms.append(top_down_transform)

def setup_front_rgb(camera_set):
    vehicle_center = pylot.simulation.utils.Location(0, 0, 0)
    forward = pylot.simulation.utils.Rotation(0, 0, 0)
