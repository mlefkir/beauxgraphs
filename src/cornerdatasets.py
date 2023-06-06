
import corner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def cornerdatasets(dataset,filename,labels,colors,name_datasets,truths=None,truth_color="#ebcf34",ncol=None,hide_quantiles=False,quantiles=[0.16, 0.5, 0.84],label_padding=0.07,scale_with_sci = True):
    """Pretty cornerplots for multiple or single datasets.
    
    
    Parameters
    ----------
    dataset : list of arrays
        List of datasets to plot. Each dataset should be an array of shape (n_samples,ndim)
    filename : str
        Filename to save the figure
    labels : list of str
        List of labels for each dimension. Should be of length ndim.
    colors : list of str
        List of colors for each dataset. Should be of length n_datasets.
    truths : list of floats, optional
        List of true values for each dimension. Should be of length ndim, by default None
    truth_color : str, optional
        Color of the true values, by default "g"
    ncol : int, optional
        Number of columns in the legend, by default None. If None, ncol = n_datasets
    hide_quantiles : bool, optional
        Hide the quantiles in the 1d histograms, by default False
    quantiles : list of floats, optional
        Quantiles to show in the 1d histograms, by default [0.16, 0.5, 0.84]
    label_padding : float, optional
        Padding between the labels and the 1d histograms, by default 0.07
    scale_with_sci : bool, optional
        Scale the labels with scientific notation, by default True
    name_datasets : list of str, optional
        List of names for each dataset. Should be of length n_datasets, by default None
    
    
    
    """

    n_datasets = len(dataset)
    
    if name_datasets is not None:
        if len(name_datasets)!=n_datasets:
            raise ValueError(f"Wrong number of names ({len(name_datasets)}) vs {n_datasets} for name_datasets")
    ndim = dataset[0].shape[-1]
    quantiles_corn = quantiles

    if hide_quantiles: quantiles_corn = None
    figure = corner.corner(dataset[0],truths=truths,truth_color=truth_color,quantiles=quantiles_corn,
                           labelpad=label_padding,labels=labels,color=colors[0],title_kwargs={"fontsize": 12},
                            hist_kwargs=dict(density=True,alpha=0.5,histtype="stepfilled",ec="k"),
                            fill_contours=False,no_fill_contours=True)


    axes = np.array(figure.axes).reshape((ndim, ndim))
    
    # for the label above 1d histograms
    loc = 1.16
    increment_loc = 0.16

    title_fmt=".2f"
    for i in range(ndim):
        q_lo, q_mid, q_hi  = corner.quantile(dataset[0][:,i],quantiles)
        q_m, q_p = q_mid - q_lo, q_hi - q_mid
        ax = axes[i, i]
        fmt = "{{0:{0}}}".format(title_fmt).format
        print(q_mid,q_m,q_p)
        # pretty 
        if q_mid>1e2 or q_mid<1e-1 :
            s = np.sign(np.log10(abs(q_mid)))
            idx = (int(abs(np.log10(abs(q_mid)))+1))*int(s)
            q_mid_trunc = q_mid *10**(-idx)
            q_m_trunc = q_m *10**(-idx)
            q_p_trunc = q_p *10**(-idx)
            title = r"${{{0}}}_{{-{1}}}^{{+{2}}}\times 10^{{{3}}}$"
            title = title.format(fmt(q_mid_trunc), fmt(q_m_trunc), fmt(q_p_trunc),idx)

            if scale_with_sci :
                if i==0 : # first column and last row
                     # set sci notation on x axis of the corresponding variable
                    axes[ndim-1,i].get_xaxis().get_offset_text().set_usetex(True)
                    axes[ndim-1,i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                    figure.canvas.draw() # necessary to access the text values...
                    offset_x = axes[ndim-1,i].get_xaxis().get_offset_text().get_text()
                    if '1e' in offset_x:
                        offset_x = offset_x.replace("1e",r"\times 10^{")+'}'
                    plt.setp(axes[ndim-1,i].get_xaxis().get_offset_text(), visible=False)
                    oldlabel_x = axes[ndim-1,i].get_xaxis().label.get_text()
                    axes[ndim-1,i].set_xlabel(oldlabel_x+r'  $\left('+offset_x.replace("$","").replace("\\mathdefault{}","").replace("\\mathdefault","").replace("−","-")+r'\right)$')


                elif i<ndim-1:
                    # set sci notation on x,y axis of the corresponding variable
                    axes[i,0].get_yaxis().get_offset_text().set_usetex(True)
                    axes[i,0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                    axes[ndim-1,i].get_xaxis().get_offset_text().set_usetex(True)
                    axes[ndim-1,i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                    figure.canvas.draw() # necessary to access the text values...
                    # store the text values
                    offset_y = axes[i,0].get_yaxis().get_offset_text().get_text()
                    offset_x = axes[ndim-1,i].get_xaxis().get_offset_text().get_text()
                    if '1e' in offset_x:
                        offset_x = offset_x.replace("1e",r"\times 10^{")+'}'
                        offset_y = offset_y.replace("1e",r"\times 10^{")+'}'

                    # hide the offsets 
                    plt.setp(axes[i,0].get_yaxis().get_offset_text(), visible=False)
                    plt.setp(axes[ndim-1,i].get_xaxis().get_offset_text(), visible=False)
                    # get the original labels
                    oldlabel_x = axes[ndim-1,i].get_xaxis().label.get_text()
                    oldlabel_y = axes[i,0].get_yaxis().label.get_text()
                    # append the offsets to the labels
                    axes[i,0].set_ylabel(oldlabel_y+r'  $\left('+offset_y.replace("$","").replace("\\mathdefault{}","").replace("\\mathdefault","").replace("−","-")+r'\right)$')
                    axes[ndim-1,i].set_xlabel(oldlabel_x+r'  $\left('+offset_x.replace("$","").replace("\\mathdefault{}","").replace("\\mathdefault","").replace("−","-")+r'\right)$')
                

        else:
            title = r"${{{0}}}_{{-{1}}}^{{+{2}}}$"
            title = title.format(fmt(q_mid), fmt(q_m), fmt(q_p))
        t = "{0} = {1}".format(labels[i], title)
        ax.text(0.5,loc,t, ha='center', va='top',fontsize=14, transform=ax.transAxes,color=colors[0])

    #---------------other datasets-------------
    
    for nda in range(1,n_datasets):
        corner.corner(dataset[nda], fig=figure,labels=labels,quantiles=quantiles_corn,color=colors[nda],
                      labelpad=label_padding,hist_kwargs=dict(density=True,alpha=0.5,histtype="stepfilled",
                      ec="k"),fill_contours=False,no_fill_contours=True)

        axes = np.array(figure.axes).reshape((ndim, ndim))
    
        loc += increment_loc
        for i in range(ndim):
            
            q_lo, q_mid, q_hi  = corner.quantile(dataset[nda][:,i],quantiles)
            q_m, q_p = q_mid - q_lo, q_hi - q_mid
            ax = axes[i, i]
            fmt = "{{0:{0}}}".format(title_fmt).format

            if q_mid>1e2 or q_mid<1e-1 :
                s = np.sign(np.log10(abs(q_mid)))
                idx = (int(abs(np.log10(abs(q_mid)))+1))*int(s)
                q_mid_trunc = q_mid *10**(-idx)
                q_m_trunc = q_m *10**(-idx)
                q_p_trunc = q_p *10**(-idx)
                title = r"${{{0}}}_{{-{1}}}^{{+{2}}}\times 10^{{{3}}}$"
                title = title.format(fmt(q_mid_trunc), fmt(q_m_trunc), fmt(q_p_trunc),idx)

                if scale_with_sci :
                    if i==0 : # first column and last row
                         # set sci notation on x axis of the corresponding variable
                        axes[ndim-1,i].get_xaxis().get_offset_text().set_usetex(True)
                        axes[ndim-1,i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                        figure.canvas.draw() # necessary to access the text values...
                        offset_x = axes[ndim-1,i].get_xaxis().get_offset_text().get_text()
                        if '1e' in offset_x:
                            offset_x = offset_x.replace("1e",r"\times 10^{")+'}'
                        plt.setp(axes[ndim-1,i].get_xaxis().get_offset_text(), visible=False)
                        oldlabel_x = axes[ndim-1,i].get_xaxis().label.get_text()
                        axes[ndim-1,i].set_xlabel(oldlabel_x+r'  $\left('+offset_x.replace("$","").replace("\\mathdefault{}","").replace("\\mathdefault","").replace("−","-")+r'\right)$')

                        
                    elif i<ndim-1:
                        # set sci notation on x,y axis of the corresponding variable
                        axes[i,0].get_yaxis().get_offset_text().set_usetex(True)
                        axes[i,0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
                        axes[ndim-1,i].get_xaxis().get_offset_text().set_usetex(True)
                        axes[ndim-1,i].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
                        figure.canvas.draw() # necessary to access the text values...
                        # store the text values
                        offset_y = axes[i,0].get_yaxis().get_offset_text().get_text()
                        offset_x = axes[ndim-1,i].get_xaxis().get_offset_text().get_text()
                        if '1e' in offset_y:
                            offset_x = offset_x.replace("1e",r"\times 10^{")+'}'
                            offset_y = offset_y.replace("1e",r"\times 10^{")+'}'

                        # hide the offsets 
                        plt.setp(axes[i,0].get_yaxis().get_offset_text(), visible=False)
                        plt.setp(axes[ndim-1,i].get_xaxis().get_offset_text(), visible=False)
                        # get the original labels
                        oldlabel_x = axes[ndim-1,i].get_xaxis().label.get_text()
                        oldlabel_y = axes[i,0].get_yaxis().label.get_text()
                        # append the offsets to the labels
                        axes[i,0].set_ylabel(oldlabel_y+r'  $\left('+offset_y.replace("$","").replace("\\mathdefault{}","").replace("\\mathdefault","").replace("−","-")+r'\right)$')
                        axes[ndim-1,i].set_xlabel(oldlabel_x+r'  $\left('+offset_x.replace("$","").replace("\\mathdefault{}","").replace("\\mathdefault","").replace("−","-")+r'\right)$')
                

            else:
                title = r"${{{0}}}_{{-{1}}}^{{+{2}}}$"
                title = title.format(fmt(q_mid), fmt(q_m), fmt(q_p))
            t = "{0} = {1}".format(labels[i], title)
            ax.text(0.5,loc,t, ha='center', va='top',fontsize=14, transform=ax.transAxes,color=colors[nda])

    if ncol is None : 
        ncol = len(colors)
    legend_elements = [Patch(facecolor=colors[nda], alpha=0.5,edgecolor=colors[nda], label=name_datasets[nda]) for nda in range(len(colors))]
    if truths is not None:
        legend_elements.append(Line2D([0], [0], color=truth_color, lw=2, label='Truth'))
    axes[ndim-1,0].legend(handles=legend_elements,ncol=ncol,loc='upper center',
                          bbox_to_anchor=(0.5, -0.0), bbox_transform=figure.transFigure)
    figure.subplots_adjust(hspace=0.15, wspace=0.15)
    figure.savefig(f"{filename}.pdf" ,bbox_inches='tight')