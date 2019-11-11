from CHECLabPy.plotting.setup import Plotter
from matplotlib import pyplot as plt
from IPython import embed


class SpectrumFitPlotter(Plotter):
    def __init__(self, n_illuminations, **kwargs):
        super().__init__(**kwargs)
        plt.close(self.fig)
        self.n_illuminations = n_illuminations
        self.fig = plt.figure(figsize=(13, 6))
        self.ax = plt.subplot2grid((3, 2), (0, 0), rowspan=3)
        self.ax_t = plt.subplot2grid((3, 2), (0, 1), rowspan=3)

    def plot(self, hist_x, hist_y, hist_edges, fit_x, fit_y, values, errors, initial):
        for i in range(self.n_illuminations):
            lambda_label = f"{values[f'lambda_{i}']:.3f} ± {errors[f'lambda_{i}']:.3f} p.e."
            color = next(self.ax._get_lines.prop_cycler)['color']
            self.ax.hist(
                hist_x,  weights=hist_y[i], bins=hist_edges, histtype='step', color=color
            )
            self.ax.plot(fit_x, fit_y[i], color=color, label=lambda_label)

        self.ax_t.axis('off')
        columns = ['Initial', 'Fit']
        rows = list(values.keys())
        cells = [['%.3g' % initial[i], '%.3f' % values[i]] for i in rows]
        for r, i in enumerate(rows):
            cells[r][1] = '%.3f ± %.3f' % (values[i], errors[i])
            # cells = [['%.3g' % coeff_initial[i], '%.3g ± %.3g' % (coeff[i], errors[i])] for i in rows]
        table = self.ax_t.table(
            cellText=cells, rowLabels=rows, colLabels=columns, loc='center'
        )
        table.set_fontsize(6)

    def finish(self):
        self.ax.legend(loc=1, frameon=True, fancybox=True, framealpha=0.7)
