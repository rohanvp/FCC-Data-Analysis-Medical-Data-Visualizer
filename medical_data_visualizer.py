import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = df=pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = np.where((df['weight']/(df['height']*df['height']/10000))>25,1,0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol']=np.select([df['cholesterol']==1,df['cholesterol']>1],[0,1],default=0)
df['gluc']=np.select([df['gluc']==1,df['gluc']>1],[0,1],default=0)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat=pd.melt(df,id_vars='cardio',value_vars=['active','alco','cholesterol','gluc','overweight','smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat=df_cat.groupby(['cardio','variable','value'])['variable'].count().reset_index(name='total')
    

    # Draw the catplot with 'sns.catplot()'
    # Get the figure for the output
    g = sns.catplot(data=df_cat,x="variable",y="total",hue="value",col="cardio",kind="bar")
    fig=g.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data

    clean_df=df.copy()
  
    clean_df=clean_df.loc[
        (clean_df['ap_lo'] <= clean_df['ap_hi']) & (clean_df['height'] >= clean_df['height'].quantile(0.025)) & (clean_df['height'] <= clean_df['height'].quantile(0.975)) & (clean_df['weight'] >= clean_df['weight'].quantile(0.025)) & (clean_df['weight'] <= clean_df['weight'].quantile(0.975))
    ]

    df_heat = clean_df

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Draw the heatmap with 'sns.heatmap()'

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Draw the heatmap with the mask and correct aspect ratio
    ax=sns.heatmap(corr, mask=mask, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5},fmt=".1f",annot=True)
    

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
