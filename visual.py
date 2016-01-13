import numpy as np

from matplotlib.widgets import Button

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import matplotlib.pyplot as plt

import colorsys

groups = [{'center': [0, 0, 0], 'name': 'one', 'radius': 1},
          {'center': [1, 1, 1], 'name': 'two', 'radius': 2},
          {'center': [2, 2, 2], 'name': 'three', 'radius': 3},
          {'center': [3, 3, 3], 'name': 'four', 'radius': 3}]

"""
input format:

groups = [
          {'center': [x1, y1, z1],
           'radius': 0.1,
            key3: val3,
            ...
            key_n: val_n
           },

           ....,

         {'center': [xm, ym, zm],
          'radius': 0.1,
           key3: val3,
           ...
           key_n: val_n
          }
         ]
"""

def get_colors(num_colors):

    colors = []
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors


class viewer_3d(object):
    def __init__(self, groups):

        points = [g['center'] for g in groups]

        self.points = points
        self.groups = groups

        # color = iter(plt.cm.rainbow(np.linspace(0, 1, len(set(deals)))))
        colors = get_colors(len(groups))

        self.fig = plt.figure(1)
        plt.rcParams['figure.figsize'] = 9, 9

        self.fig_text = plt.figure(2)

        self.fig_buttons = plt.figure(3)

        # Doing some layout with subplots:
        # fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')

        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')

        # plot main figure
        labels = []
        buttons = []
        # cursors = []

        for i_col, group in enumerate(self.groups):

            ax_button = self.fig_buttons.add_subplot(len(groups), 1, i_col + 1)
            # cursor = Cursor(ax_button, useblit=True, color='black', linewidth=2)

            c = group['center']
            r = group['radius']

            self.ax.scatter(c[0], c[1], c[2], s=1e3 * r, c=colors[i_col])

            group_button = ButtonClickProcessor(ax_button, label=i_col, color=colors[i_col], viewer=self)

            x_proj, y_proj, _ = proj3d.proj_transform(c[0], c[1], c[1], self.ax.get_proj())

            label = self.ax.annotate(str(i_col),
                                     xy=(x_proj, y_proj), xytext=(-20, 20),
                                     textcoords='offset points', ha='right', va='top', fontsize=12,
                                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                     arrowprops = dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

            labels.append(label)
            buttons.append(group_button)
            # cursors.append(cursor)

        self.labels = labels
        # self.buttons = buttons
        # self.cursors = cursors

        # lgd = self.ax.legend(loc=9, bbox_to_anchor=(0.5,0))
        # self.ax.legend()

        self.fig_buttons.canvas.draw()

        #connect events
        self.fig.canvas.mpl_connect('button_release_event', self.update_position)

    def update_position(self, e):

        labels = self.labels

        for ii, c in enumerate(self.points):

            x_proj, y_proj, _ = proj3d.proj_transform(c[0], c[1], c[2], self.ax.get_proj())
            labels[ii].xy = x_proj, y_proj

            labels[ii].update_positions(self.fig.canvas.renderer)

        self.fig.canvas.draw()


class ButtonClickProcessor(object):
    def __init__(self, axes, label, color, viewer):

        self.groups = viewer.groups
        self.fig_text = viewer.fig_text

        self.button = Button(axes, label=label, color=color)
        self.button.on_clicked(self.print_group)

    def print_group(self, event):

        print(self.button.label.get_text())

        group = self.groups[int(self.button.label.get_text())]

        self.fig_text.clf()
        self.ax_text = self.fig_text.add_subplot(111)
        # plt.rcParams['text.usetex'] = True

        y_write = np.linspace(0, 0.9, len(group.keys()))
        for ii, key in enumerate(group.keys()):
            self.ax_text.text(0, y_write[ii], str(key) + ' : ' + str(group[key]), fontsize=15, fontstyle='oblique')

        #Show it
        self.fig_text.canvas.draw()
        # plt.show()
