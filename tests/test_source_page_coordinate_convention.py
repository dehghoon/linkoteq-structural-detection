import math


def render_pixel_to_source_page(x_pixel, y_pixel, sx, sy, crop_xmin=0.0, crop_ymin=0.0):
    """Implements contracts/source-page-coordinate-convention-v0.1.md for unrotated pages."""
    return crop_xmin + x_pixel / sx, crop_ymin + y_pixel / sy


def test_full_page_100_dpi_mapping():
    # 100 dpi render of a 3456 x 2592 point page is 4800 x 3600 pixels.
    sx = sy = 100.0 / 72.0
    x, y = render_pixel_to_source_page(4800.0, 3600.0, sx, sy)
    assert math.isclose(x, 3456.0, abs_tol=1e-9)
    assert math.isclose(y, 2592.0, abs_tol=1e-9)


def test_crop_offset_is_added():
    x, y = render_pixel_to_source_page(300.0, 150.0, 1.5, 1.5, crop_xmin=700.0, crop_ymin=600.0)
    assert math.isclose(x, 900.0, abs_tol=1e-9)
    assert math.isclose(y, 700.0, abs_tol=1e-9)


def test_top_left_origin_is_stable():
    x, y = render_pixel_to_source_page(0.0, 0.0, 2.0, 2.0)
    assert (x, y) == (0.0, 0.0)
