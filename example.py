#!/usr/bin/env python3

from luminate import window, widget, datasource, draw, utility
import numpy as np


def main():
    main_window = window.Window(width=800, height=600)
    test_pattern = utility.get_test_pattern()
    draw.plot_line(test_pattern, 0, 300, 799, 300, np.array((0.0, 0.0, 0.0)))
    test_tex = datasource.ConstantDataSource(test_pattern)
    main_window.widgets.append(widget.TextureWidget(main_window, 0, 0, 800, 600, data_source=test_tex))
    main_window.run()


if __name__ == '__main__':
    main()
