import numpy as np
import pickle
import PIL.Image as Image
from collections import defaultdict
import os

import pylot.utils
from pylot.perception.segmentation.utils import transform_to_cityscapes_palette

from erdos.op import Op
from erdos.utils import setup_csv_logging, setup_logging


class CameraLoggerOp(Op):
    def __init__(self, name, flags, log_file_name=None, csv_file_name=None):
        super(CameraLoggerOp, self).__init__(name)
        self._flags = flags
        self._logger = setup_logging(self.name, log_file_name)
        self._csv_logger = setup_csv_logging(self.name + '-csv', csv_file_name)
        self._bgr_frame_cnt = 0
        self._segmented_frame_cnt = 0
        self._depth_frame_cnt = 0

        self._left_bgr_frame_cnt = 0
        self._right_bgr_frame_cnt = 0

        self._frame_cnt = defaultdict(int)

    @staticmethod
    def setup_streams(input_streams):
        input_streams.filter(pylot.utils.is_center_camera_stream).add_callback(
        CameraLoggerOp.create_bgr_frame_handler('carla-center'))
        input_streams.filter(pylot.utils.is_left_camera_stream).add_callback(
        CameraLoggerOp.on_bgr_frame_left)
        input_streams.filter(pylot.utils.is_right_camera_stream).add_callback(
        CameraLoggerOp.on_bgr_frame_right)

        input_streams.filter(
            pylot.utils.is_segmented_camera_stream).add_callback(
                CameraLoggerOp.create_segmented_frame_handler('segmeted-ck'))
        input_streams.filter(
            pylot.utils.is_depth_camera_stream).add_callback(
                CameraLoggerOp.on_depth_frame)
        return []

    def on_bgr_frame(self, msg):
        self._bgr_frame_cnt += 1
        if self._bgr_frame_cnt % self._flags.log_every_nth_frame != 0:
            return
        # Write the image.
        assert msg.encoding == 'BGR', 'Expects BGR frames'
        rgb_array = pylot.utils.bgr_to_rgb(msg.frame)
        file_name = '{}carla-center-{}.png'.format(
            self._flags.data_path, msg.timestamp.coordinates[0])
        rgb_img = Image.fromarray(np.uint8(rgb_array))
        rgb_img.save(file_name)

    def on_bgr_frame_left(self, msg):
        self._left_bgr_frame_cnt += 1
        if self._left_bgr_frame_cnt % self._flags.log_every_nth_frame != 0:
            return
        # Write the image.
        assert msg.encoding == 'BGR', 'Expects BGR frames'
        rgb_array = pylot.utils.bgr_to_rgb(msg.frame)
        file_name = '{}carla-left-{}.png'.format(
            self._flags.data_path, msg.timestamp.coordinates[0])
        rgb_img = Image.fromarray(np.uint8(rgb_array))
        rgb_img.save(file_name)

    def on_bgr_frame_right(self, msg):
        self._right_bgr_frame_cnt += 1
        if self._right_bgr_frame_cnt % self._flags.log_every_nth_frame != 0:
            return
        # Write the image.
        assert msg.encoding == 'BGR', 'Expects BGR frames'
        rgb_array = pylot.utils.bgr_to_rgb(msg.frame)
        file_name = '{}carla-right-{}.png'.format(
            self._flags.data_path, msg.timestamp.coordinates[0])
        rgb_img = Image.fromarray(np.uint8(rgb_array))
        rgb_img.save(file_name)

    def on_segmented_frame(self, msg):
        self._segmented_frame_cnt += 1
        if self._segmented_frame_cnt % self._flags.log_every_nth_frame != 0:
            return
        frame = transform_to_cityscapes_palette(msg.frame)
        # Write the segmented image.
        img = Image.fromarray(np.uint8(frame))
        file_name = '{}carla-segmented-{}.png'.format(
            self._flags.data_path, msg.timestamp.coordinates[0])
        img.save(file_name)

    def on_depth_frame(self, msg):
        self._depth_frame_cnt += 1
        if self._depth_frame_cnt % self._flags.log_every_nth_frame != 0:
            return
        # Write the depth information.
        file_name = '{}carla-depth-{}.pkl'.format(
            self._flags.data_path, msg.timestamp.coordinates[0])
        pickle.dump(msg.frame,
                    open(file_name, 'wb'),
                    protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def create_bgr_frame_handler(camera_name):
        '''
        create a handler that writes rgb image frames to disk with file name in the form of
            <data_path>/<identifier>-<time_stamp>.png
        This allows us to easily add more handlers of many cameras.
        '''

        def on_bgr_frame(self, msg):
            # log every nth frame
            self._frame_cnt[camera_name] += 1
            if self._frame_cnt[camera_name] % self._flags.log_every_nth_frame != 0:
                return

            # Write the image.
            assert msg.encoding == 'BGR', 'Expects BGR frames'
            rgb_array = pylot.utils.bgr_to_rgb(msg.frame)
            file_name = '{}-{}.png'.format(
                camera_name, msg.timestamp.coordinates[0])
            path = os.path.join(self._flags.data_path, file_name)
            rgb_img = Image.fromarray(np.uint8(rgb_array))
            rgb_img.save(path)

        return on_bgr_frame

    @staticmethod
    def create_segmented_frame_handler(camera_name):
        '''
        create a handler that writes segmentation frames to disk with file name in the form of
            <data_path>/<identifier>-<time_stamp>.png
        This allows us to easily add more handlers of many cameras.
        '''

        def on_segmented_frame(self, msg):

            # log every nth frame
            self._frame_cnt[camera_name] += 1
            if self._frame_cnt[camera_name] % self._flags.log_every_nth_frame != 0:
                return

            # Write the segmented image.
            frame = transform_to_cityscapes_palette(msg.frame)
            img = Image.fromarray(np.uint8(frame))
            file_name = '{}-{}.png'.format(
                camera_name, msg.timestamp.coordinates[0])
            path = os.path.join(self._flags.data_path, file_name)
            img.save(path)

        return on_segmented_frame

    @staticmethod
    def create_depth_frame_handler(camera_name):
        '''
        create a handler that writes depth frames to disk with file name in the form of
            <data_path>/<identifier>-<time_stamp>.png
        This allows us to easily add more handlers of many cameras.
        '''

        def on_depth_frame(self, msg):
            # log every nth frame
            self._frame_cnt[camera_name] += 1
            if self._frame_cnt[camera_name] % self._flags.log_every_nth_frame != 0:
                return

            # Write the depth information.
            file_name = '{}-{}.pkl'.format(
                camera_name, msg.timestamp.coordinates[0])
            path = os.path.join(self._flags.data_path, file_name)
            pickle.dump(msg.frame,
                        open(path, 'wb'),
                        protocol=pickle.HIGHEST_PROTOCOL)

        return on_depth_frame