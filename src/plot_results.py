import argparse
import pandas as pd
import sys

from matplotlib import pyplot as plt

SMALL_SIZE = 10
MEDIUM_SIZE = 16
BIGGER_SIZE = 16

#plt.rc('font', size=BIGGER_SIZE)         # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title



def generate_figures(all_results, all_auprcs, figfile) :

    my_colors = [
        'tab:blue',
        'tab:olive',
        'tab:orange',
        'tab:green',
        'tab:red',
        'tab:purple',
        'tab:brown',
        'tab:pink',
        'tab:gray'
    ]
    my_markers = 'ov^s+*xdp'
    color_dict = {}
    marker_dict = {}
    for method, col, mrk in zip(all_auprcs['method'], my_colors, my_markers) :
        color_dict[method] = col
        marker_dict[method] = mrk

    grouped_pr_curves = all_results.groupby(['method'])

    plt.figure(1, figsize=(5,12))
    #   a. Plot PR-curve for each method (line plots) 
    plt.subplot(311)
    for method, values in grouped_pr_curves :
        plt.plot(
            values['recall'], 
            values['precision'],
            label=method,
            color=color_dict[method],
            marker=marker_dict[method],
            markersize=10
        )
    plt.legend(loc='lower left', framealpha=0.1)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Recall vs. Precision', fontsize=BIGGER_SIZE)

    #   b. Plot AUPRC for each method (bar plots)
    plt.subplot(312)
    color_list = [ color_dict[m] for m in all_auprcs['method'] ]
    yerrs_list = all_auprcs['auprc_std'] if 'auprc_std' in all_auprcs else None
    plt.bar(
        all_auprcs['method'],
        all_auprcs['auprc'],
        color=color_list,
        yerr=yerrs_list,
        ecolor='black',
        capsize=7
    )
    plt.xticks(rotation=30)
    plt.xlabel('Method')
    plt.ylabel('AUPRC')
    plt.title('Area under Recall vs. Precision Curve', fontsize=BIGGER_SIZE)

    #   c. #queries/second curve for each method (line plots)
    plt.subplot(313)
    for method, values in grouped_pr_curves :
        plt.plot(
            values['recall'], 
            values['nqueries_per_sec'],
            label=method,
            color=color_dict[method],
            marker=marker_dict[method],
            markersize=10
        )
    plt.yscale('log')
    plt.xlabel('Recall')
    plt.ylabel('#queries/sec')
    plt.title('Recall vs. Num. queries per second', fontsize=BIGGER_SIZE)

    plt.tight_layout()
    print('Plots generated, saving figures in \'%s\'' % figfile)
    plt.savefig(fname=figfile, format='png')    
# -- end function


def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r', '--results_file', help='File containing the PR-curve', type=str
    )
    parser.add_argument(
        '-a', '--auprc_results_file', help='File containing the AUPRC', type=str
    )
    parser.add_argument(
        '-g',
        '--figures_file',
        help='File where the figures will be output for this experiment',
        type=str
    )
    args = parser.parse_args()

    results_df = pd.read_csv(args.results_file)
    auprc_df = pd.read_csv(args.auprc_results_file)

    generate_figures(results_df, auprc_df, args.figures_file)

if __name__ == '__main__' :
    status = main()
    sys.exit(status)
# -- end function
