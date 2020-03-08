from PIL import Image, ImageFilter, ImageDraw
from math import sqrt
import sys
import os

sys.path.insert(0, os.pardir)

FILENAME = "art3.jpg"

WHITE_PIXEL, BLACK_PIXEL = 255, 0

img_b_w_contour = Image.open(FILENAME).filter(ImageFilter.GaussianBlur(radius=4)).convert('L').point(
    lambda x: 0 if x < 128 else 255, '1')
IMAGE_WIDTH, IMAGE_HEIGHT = img_b_w_contour.size
IMG_SIZE_KOEF = IMAGE_WIDTH
img_b_w_contour.thumbnail((IMAGE_WIDTH // 3, IMAGE_HEIGHT // 3))
img_b_w_contour = img_b_w_contour.filter(ImageFilter.CONTOUR)
IMAGE_WIDTH, IMAGE_HEIGHT = img_b_w_contour.size
IMG_SIZE_KOEF = IMG_SIZE_KOEF * 1. / IMAGE_WIDTH

img_b_w_matrix = img_b_w_contour.load()

img_blur_with_objects_rects = Image.open(FILENAME).filter(ImageFilter.GaussianBlur(radius=4))

lowest, highest, most_right, most_left, start_point, travelled = -1, -1, -1, -1, (-1, -1), [
    [False for _ in range(IMAGE_HEIGHT)] for _ in
    range(IMAGE_WIDTH)]


def write_rect_corner_pixels_cells(column, row):
    global img_b_w_contour, lowest, highest, most_left, most_right, travelled
    travelled[column][row] = True

    if column > most_right or most_right == -1:
        most_right = column
    if column < most_left or most_left == -1:
        most_left = column
    if row > lowest or lowest == -1:
        lowest = row
    if row < highest or highest == -1:
        highest = row

    if column > 0 and img_b_w_matrix[column - 1, row] == BLACK_PIXEL and not travelled[column - 1][row]:
        write_rect_corner_pixels_cells(column - 1, row)
    if row > 0 and img_b_w_matrix[column, row - 1] == BLACK_PIXEL and not travelled[column][row - 1]:
        write_rect_corner_pixels_cells(column, row - 1)
    if column < IMAGE_WIDTH - 1 and img_b_w_matrix[column + 1, row] == BLACK_PIXEL and not travelled[column + 1][row]:
        write_rect_corner_pixels_cells(column + 1, row)
    if row < IMAGE_HEIGHT - 1 and img_b_w_matrix[column, row + 1] == BLACK_PIXEL and not travelled[column][row + 1]:
        write_rect_corner_pixels_cells(column, row + 1)


RECT_CONTOUR_WIDTH, RECT_OUTLINE_TYPE = 3, (255, 200, 0)

MIN_OBJECT_SIZE = 300

objects_rectangles = []

for column in range(IMAGE_WIDTH):
    for row in range(IMAGE_HEIGHT):
        if not travelled[column][row] and img_b_w_matrix[column, row] == BLACK_PIXEL:
            try:
                lowest, highest, most_right, most_left, start_point = -1, -1, -1, -1, (column, row)
                write_rect_corner_pixels_cells(column, row)
                size = (most_right - most_left) * (lowest - highest)
                if size < MIN_OBJECT_SIZE:
                    # too small
                    raise RuntimeError()
                else:
                    objects_rectangles.append((
                        tuple(
                            map(int,
                                map(round, [i * IMG_SIZE_KOEF for i in [most_left, highest, most_right, lowest]]))),
                        (column, row))
                    )
            except RuntimeError:
                # too big
                ImageDraw.floodfill(img_b_w_contour, (column, row), 255)

img_blur_matrix = Image.open(FILENAME).load()

min_white_color_rgb, max_black_color_rgb = (205, 205, 205), (90, 90, 90)
max_another_pixels_koef = 5.
the_right_objects_rects = []

for object_rect in objects_rectangles:
    rect_error = 0
    for i in range(object_rect[0][0], object_rect[0][2] + 1):
        for j in range(object_rect[0][1], object_rect[0][3] + 1):
            checking_pixel = img_blur_matrix[i, j]
            if max_black_color_rgb[0] < checking_pixel[0] < min_white_color_rgb[0] or \
                    max_black_color_rgb[1] < checking_pixel[1] < min_white_color_rgb[1] or \
                    max_black_color_rgb[2] < checking_pixel[2] < min_white_color_rgb[2]:
                rect_error += 1
    rect_square = (object_rect[0][2] - object_rect[0][0] + 1) * (object_rect[0][3] - object_rect[0][1] + 1)
    if rect_square / max_another_pixels_koef > rect_error:
        the_right_objects_rects.append(object_rect)
    else:
        ImageDraw.floodfill(img_b_w_contour, object_rect[-1], 255)

del objects_rectangles, travelled, start_point

objects_rectangles, most_l_u, most_l_d, most_r_u, most_r_d = list(), tuple(), tuple(), tuple(), tuple()
rect_corner_l_u, rect_corner_l_d, rect_corner_r_u, rect_corner_r_d = None, None, None, None
IMAGE_WIDTH, IMAGE_HEIGHT = img_b_w_contour.size
travelled = [[False for _ in range(IMAGE_HEIGHT)] for _ in range(IMAGE_WIDTH)]


def get_section_length(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def write_figure_corner_pixels_cells(column, row):
    global img_b_w_contour, most_l_u, most_l_d, most_r_u, most_r_d, travelled, rect_corner_l_u, rect_corner_l_d, rect_corner_r_d, rect_corner_r_u

    travelled[column][row] = True

    if not most_l_u or get_section_length(most_l_u, rect_corner_l_u) > get_section_length((column, row),
                                                                                          rect_corner_l_u):
        most_l_u = (column, row)
    if not most_l_d or get_section_length(most_l_d, rect_corner_l_d) > get_section_length((column, row),
                                                                                          rect_corner_l_d):
        most_l_d = (column, row)
    if not most_r_d or get_section_length(most_r_d, rect_corner_r_d) > get_section_length((column, row),
                                                                                          rect_corner_r_d):
        most_r_d = (column, row)
    if not most_r_u or get_section_length(most_r_u, rect_corner_r_u) > get_section_length((column, row),
                                                                                          rect_corner_r_u):
        most_r_u = (column, row)

    if column > 0 and img_b_w_matrix[column - 1, row] == BLACK_PIXEL and not travelled[column - 1][row]:
        write_figure_corner_pixels_cells(column - 1, row)
    if row > 0 and img_b_w_matrix[column, row - 1] == BLACK_PIXEL and not travelled[column][row - 1]:
        write_figure_corner_pixels_cells(column, row - 1)
    if column < IMAGE_WIDTH - 1 and img_b_w_matrix[column + 1, row] == BLACK_PIXEL and not travelled[column + 1][row]:
        write_figure_corner_pixels_cells(column + 1, row)
    if row < IMAGE_HEIGHT - 1 and img_b_w_matrix[column, row + 1] == BLACK_PIXEL and not travelled[column][row + 1]:
        write_figure_corner_pixels_cells(column, row + 1)


object_shapes_corners = list()

for rect in the_right_objects_rects:
    most_l_u, most_l_d, most_r_u, most_r_d = (), (), (), ()
    end_for = False
    for i in range(rect[0][0] // 3, (rect[0][2] + 1) // 3):
        for j in range(rect[0][1] // 3, (rect[0][3] + 1) // 3):
            if img_b_w_matrix[i, j] == BLACK_PIXEL:
                rect_corner_l_u, rect_corner_l_d, rect_corner_r_u, rect_corner_r_d = \
                    (rect[0][0] // 3, rect[0][1] // 3), (rect[0][0] // 3, rect[0][3] // 3), (
                        rect[0][2] // 3, rect[0][1] // 3), (rect[0][2] // 3, rect[0][3] // 3)
                write_figure_corner_pixels_cells(i, j)
                ImageDraw.floodfill(img_b_w_contour, (i, j), WHITE_PIXEL)
                end_for = True
                break
        if end_for:
            break
    object_shapes_corners.append(
        tuple(map(tuple, [[int(i * IMG_SIZE_KOEF) for i in j] for j in [most_l_u, most_r_u, most_r_d, most_l_d]])))

del img_b_w_contour, img_b_w_matrix

max_around_black_rgb_color = (100, 100, 100)
max_another_color_pixels_koef = 4.


def is_this_like_black(color):
    return color[0] < max_around_black_rgb_color[0] and color[1] < max_around_black_rgb_color[1] and color[2] < \
           max_around_black_rgb_color[2]


def is_around_black_pixels(column, row):
    global img_blur_matrix

    if not is_this_like_black(img_blur_matrix[column, row]):
        return False

    return True


the_right_objects_shapes_corners = list()

for shape_corner_index in range(len(object_shapes_corners)):
    color_error, whole = 0, 0
    for i in range(4):
        corner1, corner2 = object_shapes_corners[shape_corner_index][i - 1], \
                           object_shapes_corners[shape_corner_index][i]
        dif_x, dif_y = corner2[0] - corner1[0], corner2[1] - corner1[1]
        steps_amount = max(abs(dif_x), abs(dif_y))
        whole += steps_amount
        step_x, step_y = float(dif_x) / float(steps_amount), float(dif_y) / float(steps_amount)
        for step in range(steps_amount):
            if not is_around_black_pixels(int(corner2[0] - step * step_x), int(corner2[1] - step * step_y)):
                color_error += 1
    if color_error < whole / max_another_color_pixels_koef:
        objects_rectangles.append(the_right_objects_rects[shape_corner_index])
        the_right_objects_shapes_corners.append(object_shapes_corners[shape_corner_index])

the_right_objects_rects, object_shapes_corners = list(), list()

# we do divide the biggest value into the smallest
section_max_deviation_in_figure_percents = 25.

for figure_index in range(len(the_right_objects_shapes_corners)):
    is_norm = True
    cur_shape = the_right_objects_shapes_corners[figure_index]
    sections_lengths = [get_section_length(cur_shape[0], cur_shape[1]), get_section_length(cur_shape[1], cur_shape[2]),
                        get_section_length(cur_shape[2], cur_shape[3]), get_section_length(cur_shape[3], cur_shape[0])]
    for section1 in sections_lengths:
        if not is_norm:
            break
        for section2 in sections_lengths:
            if 1. * max(section1, section2) / min(section1, section2) > \
                    (1. + section_max_deviation_in_figure_percents / 100.):
                is_norm = False
                break
    diag1, diag2 = get_section_length(cur_shape[0], cur_shape[2]), get_section_length(cur_shape[1], cur_shape[3])
    if 1. * max(diag1, diag2) / min(diag1, diag2) > (1. + section_max_deviation_in_figure_percents / 100.):
        is_norm = False
    if is_norm:
        the_right_objects_rects.append(objects_rectangles[figure_index])
        object_shapes_corners.append(cur_shape)

row_image_for_presentation = Image.open(FILENAME)

for object_rect in the_right_objects_rects:
    ImageDraw.Draw(row_image_for_presentation).rectangle(object_rect[0], outline=RECT_OUTLINE_TYPE,
                                                         width=RECT_CONTOUR_WIDTH)

# for shape_corner in object_shapes_corners:
#    for point in shape_corner:
#        temp = (point[0], point[1], point[0] + 1, point[1] + 1)
#        img_draw.line(temp, fill='blue', width=3)

row_image_for_presentation.show()

del img_blur_with_objects_rects
