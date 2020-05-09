import sys
import os

from PIL import Image
import numpy as np


def create_dir_if_not_exists(directory):
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass


def crop_image_and_save(image_from, image_to, *, before_crop_margin=0, after_crop_margin=0):
    """
    crop image removed black margins around the image
    """
    print('cropping image {} ...'.format(image_from))
    image = Image.open(image_from)
    image = image.convert('RGB')
    data = np.array(image)
    rgb_data = data[:, :, :3]

    shape = rgb_data.shape
    print('image_shape:', shape)
    width = shape[1]
    height = shape[0]

    rgb_data = rgb_data[
        before_crop_margin: height - before_crop_margin, before_crop_margin: width - before_crop_margin, :]

    shape = rgb_data.shape
    width = shape[1]
    height = shape[0]

    mid_width = width // 2
    mid_height = height // 2

    height_from_top = 0
    for i in range(height):
        rgb_point = rgb_data[i, mid_width]
        if not np.array_equal(rgb_point, np.array([0, 0, 0])):
            break
        height_from_top += 1

    height_from_bottom = 0
    for i in range(height-1, -1, -1):
        rgb_point = rgb_data[i, mid_width]
        if not np.array_equal(rgb_point, np.array([0, 0, 0])):
            break
        height_from_bottom += 1

    width_from_left = 0
    for i in range(width):
        rgb_point = rgb_data[mid_height, i]
        if not np.array_equal(rgb_point, np.array([0, 0, 0])):
            break
        width_from_left += 1

    width_from_right = 0
    for i in range(width-1, -1, -1):
        rgb_point = rgb_data[mid_height, i]
        if not np.array_equal(rgb_point, np.array([0, 0, 0])):
            break
        width_from_right += 1

    left = width_from_left + after_crop_margin
    top = height_from_top + after_crop_margin
    right = width - width_from_right - after_crop_margin
    bottom = height - height_from_bottom - after_crop_margin

    print('cropped to -> left: {}, top: {}, right: {}, bottom: {}'.format(left, top, right, bottom))

    cropped_data = rgb_data[top:bottom, left:right, :]

    cropped = Image.fromarray(cropped_data)
    cropped.save(image_to)
    print('cropped image saved to {}'.format(image_to))


def crop_images_in_directory(from_, to_):
    create_dir_if_not_exists(to_)
    for f_name in os.listdir(from_):
        crop_image_and_save('{}/{}'.format(from_, f_name), '{}/{}'.format(to_, f_name),
                            before_crop_margin=30, after_crop_margin=10)



if __name__ == '__main__':
    argv = sys.argv
    dir_from = argv[1]
    dir_to = argv[2]

    crop_images_in_directory(dir_from, dir_to)
