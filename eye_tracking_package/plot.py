import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class Plot:
    """Class that represents and creates the different plots needed for the visualization of the data."""

    @ staticmethod
    def make_barplot(data_frame, figure_save_path, title=None, xlabel=None, ylabel=None):
        """
        Create a barplot out of a data frame and save its figure.

        Args:
            data_frame: Data frame containing the data from which the plot will be made.
            figure_save_path: Path where the figure of the plot will be saved.
            title (optional): Plot title written on the figure.
            xlabel (optional): Label of the x-axis.
            ylabel (optional): Label of the y-axis.
        """

        sns.set(style='whitegrid')

        plot = sns.barplot(data=data_frame,
                           capsize=0.1,  # length of the caps at the endpoint of the confidence interval bar
                           errwidth=1.5,  # width of the confidence interval bar
                           ci=95,  # size of the confidence interval
                           palette='PuBu'  # colors of the bars
                           )

        # write the labels vertically
        plot.set_xticklabels(plot.get_xticklabels(), rotation=90, horizontalalignment='right')

        # write the title of the plots and the labels of the axis
        if title:
            plot.set_title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)

        figure = plot.get_figure()
        figure.savefig(figure_save_path, bbox_inches='tight')

        plt.show(block=False)

    @ staticmethod
    def make_boxplot(data_frame, figure_save_path, title=None, xlabel=None, ylabel=None):
        """
        Create a box plot out of a data frame and save its figure.

        Args:
            data_frame: Data frame containing the data from which the plot will be made.
            figure_save_path: Path where the figure of the plot will be saved.
            title (optional): Plot title written on the figure.
            xlabel (optional): Label of the x-axis.
            ylabel (optional): Label of the y-axis.
        """

        sns.set(style='whitegrid')

        plot = sns.boxplot(data=data_frame,
                           palette='PuBu'  # colors of the boxes
                           )

        # write the labels vertically
        plot.set_xticklabels(plot.get_xticklabels(), rotation=90, horizontalalignment='right')

        # write the title of the plot and the labels of the axis
        if title:
            plot.set_title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)

        figure = plot.get_figure()
        figure.savefig(figure_save_path, bbox_inches='tight')

        plt.show(block=False)

    @ staticmethod
    def make_heatmap(data_frame, figure_save_path, title=None, xlabel=None, ylabel=None):
        """
        Create a heat map out of a data frame and save its figure.

        Args:
            data_frame: Data frame containing the data from which the plot will be made.
            figure_save_path: Path where the figure of the plot will be saved.
            title (optional): Plot title written on the figure.
            xlabel (optional): Label of the x-axis.
            ylabel (optional): Label of the y-axis.
        """

        plot = sns.heatmap(data=data_frame,
                           vmin=0, vmax=1,  # max and min value
                           annot=True,  # annotate each cell
                           linewidths=.5,  # width of the line between each cell
                           cmap='PuBu',  # color of the cells
                           cbar=False,  # bar showing the colors
                           fmt='.2%',  # formatting of the annotation
                           )

        # write the title of the plot and the labels of the axis
        if title:
            plot.set_title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)

        figure = plot.get_figure()
        figure.savefig(figure_save_path, bbox_inches='tight')

        plt.show(block=False)

    @ staticmethod
    def make_pieplot(data_vector, labels_list, figure_save_path, title=None):
        """
        Create a pie plot out of a vector and a list of labels and save its figure.

        Args:
            data_vector: Vector containing the data from which the plot will be made.
            labels_list: List containing the labels that corresponds to the data.
            figure_save_path: Path where the figure of the plot will be saved.
            title (optional): Plot title written on the figure.
        """

        # set the offset of each wedge
        explode = np.full(len(data_vector), 0.001)

        # set the colors of the wedges
        colors = ['midnightblue', 'paleturquoise', 'blue',
                  'deepskyblue', 'royalblue', 'lightcyan',
                  'steelblue', 'darkslateblue', 'lightblue'
                  ]

        # add a pie plot
        patches, texts = plt.pie(x=data_vector,
                                 startangle=0,  # start angle of the first wedge
                                 explode=explode,  # offset of the wedges
                                 colors=colors  # colors of the wedges
                                 )

        # add a list of the labels with their corresponding percentage
        percent = data_vector / data_vector.sum()
        labels = ['{0} - {1:.1%}'.format(i, j) for i, j in zip(labels_list, percent)]
        plt.legend(patches,
                   labels,
                   loc='center left',
                   bbox_to_anchor=(1, 0.5)
                   )

        # write the title of the plot
        if title:
            plt.title(title)

        plt.savefig(figure_save_path, bbox_inches='tight')

        plt.show(block=False)
