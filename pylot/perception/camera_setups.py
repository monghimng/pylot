import pylot

FRONT = 'front'

class CameraConfig:

    def __init__(self, rgb=[], segmented=[], depth=[], rgb_transforms=[], segmented_transforms=[], depth_transforms=[]):
        self.rgb_camera_names = rgb
        self.segmented_camera_names = segmented
        self.depth_camera_names = depth

        self.rgb_camera_transforms = rgb_transforms
        self.segmented_camera_transforms = segmented_transforms
        self.depth_camera_transforms = depth_transforms

def get_camera_setups(setup_flag):

    cfg = CameraConfig()

    if 'top_down_segmented' in setup_flag:
        setup_top_down_segmented(cfg)
    if FRONT in setup_flag:
        setup_front_rgb(cfg)
    return cfg

def setup_top_down_segmented(cfg):
    top_down_location = pylot.simulation.utils.Location(0, 0, 30)  # x meters above the vehicle center
    top_down_rotation = pylot.simulation.utils.Rotation(-90, 0, 0)  # face down
    top_down_transform = pylot.simulation.utils.Transform(top_down_location, top_down_rotation)
    cfg.segmented_camera_names.append('top_down_segmented')
    cfg.segmented_camera_transforms.append(top_down_transform)

def setup_front_rgb(cfg):
    loc = pylot.simulation.utils.Location(0, 0, 1.4)
    forward = pylot.simulation.utils.Rotation(0, 0, 0)
    transform = pylot.simulation.utils.Transform(loc, forward)
    cfg.rgb_camera_names.append('carla-center')
    cfg.rgb_camera_transforms.append(transform)
