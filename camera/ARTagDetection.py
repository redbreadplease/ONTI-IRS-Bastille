from PIL import Image, ImageFilter, ImageDraw

FILENAME = "examples/art3.jpg"

WHITE_PIXEL, BLACK_PIXEL = 255, 0

IMG_SIZE_KOEF = 3

img_b_w_contour = Image.open(FILENAME).filter(ImageFilter.GaussianBlur(radius=4)).convert('L').point(
    lambda x: 0 if x < 128 else 255, '1')
IMAGE_WIDTH, IMAGE_HEIGHT = img_b_w_contour.size
img_b_w_contour.thumbnail((IMAGE_WIDTH // IMG_SIZE_KOEF, IMAGE_HEIGHT // IMG_SIZE_KOEF))
img_b_w_contour = img_b_w_contour.filter(ImageFilter.CONTOUR)
IMAGE_WIDTH, IMAGE_HEIGHT = img_b_w_contour.size

img_matrix = img_b_w_contour.load()

img = Image.open("art3.jpg").filter(ImageFilter.GaussianBlur(radius=4))
img_draw = ImageDraw.Draw(img)

lowest, highest, most_right, most_left, travelled = -1, -1, -1, -1, [[False for _ in range(IMAGE_HEIGHT)] for _ in
                                                                     range(IMAGE_WIDTH)]


def write_corner_pixels_cells(column, row):
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

    if column > 0 and img_matrix[column - 1, row] == BLACK_PIXEL and not travelled[column - 1][row]:
        write_corner_pixels_cells(column - 1, row)
    if row > 0 and img_matrix[column, row - 1] == BLACK_PIXEL and not travelled[column][row - 1]:
        write_corner_pixels_cells(column, row - 1)
    if column < IMAGE_WIDTH - 1 and img_matrix[column + 1, row] == BLACK_PIXEL and not travelled[column + 1][row]:
        write_corner_pixels_cells(column + 1, row)
    if row < IMAGE_HEIGHT - 1 and img_matrix[column, row + 1] == BLACK_PIXEL and not travelled[column][row + 1]:
        write_corner_pixels_cells(column, row + 1)


RECT_CONTOUR_WIDTH, RECT_OUTLINE_TYPE = 3, 'red'
MIN_OBJECT_SIZE = 300

objects_rectangles = []

for column in range(IMAGE_WIDTH):
    for row in range(IMAGE_HEIGHT):
        if img_matrix[column, row] == BLACK_PIXEL:
            try:
                lowest, highest, most_right, most_left = -1, -1, -1, -1
                write_corner_pixels_cells(column, row)
                objects_rectangles.append([most_left, highest, most_right, lowest])
                print objects_rectangles[-1]
                try:
                    size = (most_right - most_left) * (lowest - highest)
                    if size < MIN_OBJECT_SIZE:
                        # too small
                        raise SystemError()
                    img_draw.rectangle((most_left * IMG_SIZE_KOEF, highest * IMG_SIZE_KOEF, most_right * IMG_SIZE_KOEF,
                                        lowest * IMG_SIZE_KOEF),
                                       outline=RECT_OUTLINE_TYPE, width=RECT_CONTOUR_WIDTH)
                except SystemError:
                    # contour length too big or too small
                    ImageDraw.floodfill(img_b_w_contour, (column, row), 255)
            except RuntimeError:
                # too big
                ImageDraw.floodfill(img_b_w_contour, (column, row), 255)
img.show()
