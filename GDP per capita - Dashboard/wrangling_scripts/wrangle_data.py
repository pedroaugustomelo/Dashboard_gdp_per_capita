import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`
def clean_data(dataset):
    """reads dataset and return a cleaned DataFrame

    Args:
      dataset: name of the dataset
    
    Returns: 

      df: dataset cleaned
   
    """
    #read csv and select top 10 economies
    df = pd.read_csv(dataset)

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Russian Federation']
    df = df[df['Country'].isin(top10country)]

    # melt year columns  and convert year to date time
    df.drop(['Country Code', '2019'], axis= 'columns', inplace= True)
    value_variables = df.loc['1990': '2018']
    df_melt = df.melt(id_vars='Country', value_vars = value_variables)
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt



def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    

    # first chart plots gdp per capita from 1990 to 2018 in top 10 economies 
    # as a line chart
    
    graph_one = []
    df = clean_data("data/GDP.csv")
    df.columns = ['country','year','gdp_per_capita']
    df_sort = df.loc[df['year'] == "2018"]
    df_sort = df.sort_values(by ='gdp_per_capita', ascending = False )
    countrylist = df_sort.country.unique().tolist()

    for country in countrylist:

      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].gdp_per_capita.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )
    
    

    layout_one = dict(title = 'Change in GDP per capita in selected countries <br> 1990 to 2018',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=5),
                yaxis = dict(title = 'GDP per capita'),
                )

# second chart plots Brazilian's GDP per capita growth from 1990 to 2018
    
    graph_two = []
    df = clean_data("data/GDP.csv")
    df.columns = ['country','year','gdp_per_capita']
    df = df.loc[df['country'] == "Brazil"]
    df['gdp_growth'] = df["gdp_per_capita"].pct_change()
    x_val = df.year.tolist()
    y_val = df.gdp_growth.tolist()

    graph_two.append(
      go.Scatter(
      x = x_val,
      y = y_val,
      )
    )

    layout_two = dict(title = 'GDP per capita growth rate <br> Brazil',
                xaxis = dict(title = 'Year',autotick=False, tick0=1990, dtick=5),
                yaxis = dict(title = ' Growth rate'),
                )


# third chart plots the ratio between Brazil's GDP per capita and China's GDP per capita
    graph_three = []
    df = clean_data("data/GDP.csv")
    df.columns = ['country','year','gdp_per_capita']
    gdp_brazil  =  df[df['country'] == 'Brazil'].gdp_per_capita.tolist()
    gdp_china   =  df[df['country'] == 'China'].gdp_per_capita.tolist()
    ratio_gdp = list(map(lambda v1, v2: v1/v2, gdp_brazil, gdp_china))

    x_val = df[df['country'] == country].year.tolist()
    y_val =  ratio_gdp
    graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          
          )
      )
    

    graph_three.append(
      go.Scatter(
      x = x_val,
      y = y_val,
      marker=dict(
            color='Red')
      )
    )

    layout_three = dict(title = 'GDP per capita ratio <br> Brazil vs. China',
                xaxis = dict(title = 'Year',autotick=False, tick0=1990, dtick=5),
                yaxis = dict(title = ' Ratio'),
                )
    
# fourth chart 
    graph_four = []
    df = clean_data("data/GDP.csv")
    df.columns = ['country','year','gdp_per_capita']
    df = df.sort_values(['country', 'year'])
    df['pct'] = df.groupby('country')['gdp_per_capita'].pct_change()
    average_growth_gdp = df.groupby('country')['pct'].mean().tolist()
    countrylist = df.country.unique().tolist()
    
    graph_four.append(
          go.Bar(
          x = countrylist,
          y = average_growth_gdp,
          name = country,
          marker=dict(
            color='Gold')
          )
      )
    

    layout_four = dict(title = 'Average GDP per capita Growth Rate <br> 1990 to 2018',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'Average Growth Rate'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures