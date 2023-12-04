import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit
import os

# opening the data as dataframe
voting_path = os.path.abspath('data/eurovision_song_contest_1975_2019.xlsx')
lan_sim_path = os.path.abspath('data/dicl.csv')
iso_path = os.path.abspath('data/iso_country.csv')

world_lan_path = os.path.abspath('data/World_Languages.csv')

voting_data = pd.read_excel(voting_path)
lan_sim_data = pd.read_csv(lan_sim_path)
iso_data = pd.read_csv(iso_path)


# adding country name to language similarity data
lan_sim_data = pd.merge(lan_sim_data, iso_data[['alpha-3', 'name']], 
                        left_on='ISO3', right_on='alpha-3')
lan_sim_data.drop('alpha-3', axis=1, inplace=True)
lan_sim_data = pd.merge(lan_sim_data, iso_data[['alpha-3', 'name']], 
                        left_on='ISO3_2', right_on='alpha-3')
lan_sim_data.drop('alpha-3', axis=1, inplace=True)

# cleaning voting data
# renaming wrong/differently named country
# renameing yugoslavia/Serbia & Montenegro as serbia to treat them 
# as the same language as serbia
replace_dict = {'From country': {
    'The Netherlands': 'Netherlands','The Netherands':'Netherlands',
    'Bosnia & Herzegovina': 'Bosnia and Herzegovina',
    'Czech Republic': 'Czechia', 'F.Y.R. Macedonia': 'North Macedonia',
    'Macedonia':'North Macedonia',
    'United Kingdom':'United Kingdom of Great Britain and Northern Ireland',
    'Moldova': 'Moldova, Republic of', 
    'Russia': 'Russian Federation'},
   'To country': {
       'The Netherlands': 'Netherlands','The Netherands':'Netherlands',
       'Bosnia & Herzegovina': 'Bosnia and Herzegovina',
       'Czech Republic': 'Czechia', 'F.Y.R. Macedonia': 'North Macedonia',
       'Macedonia':'North Macedonia',
       'United Kingdom':'United Kingdom of Great Britain and Northern Ireland',
       'Moldova': 'Moldova, Republic of',
       'Russia': 'Russian Federation'}}

voting_data.replace(replace_dict, inplace=True)

replace_dict2 = {'Country': {
    'Czech Republic': 'Czechia',
    'Macedonia':'North Macedonia',
    'United Kingdom':'United Kingdom of Great Britain and Northern Ireland',
    'Moldova': 'Moldova, Republic of', 'Yugoslavia': 'Serbia',
    'Russia': 'Russian Federation', 'Republic of Serbia': 'Serbia'},
}

# combined data for analysis
votes_lan = pd.merge(voting_data, lan_sim_data,
                     left_on=['From country', 'To country'],
                     right_on=['name_x', 'name_y'])

votes_lan.drop(columns=['name_x', 'name_y',
                        'ISO3', 'ISO3_2'], inplace=True)

sns.set_context('notebook')
sns.set_style('darkgrid')

print(votes_lan.head())
filtered_data = votes_lan[(votes_lan['Year'] == 2019) & (votes_lan['Jury or Televoting'] == 'T')]

sns.set(style="ticks", palette="gray")

votes_lan.rename(columns={'Points      ':'Points'}, inplace=True)
mean_sim = votes_lan.groupby('Points', as_index= False)['cl'].mean()
mean_sim['Points'] = pd.to_numeric(mean_sim['Points'])

mean_sim['cl'] = mean_sim['cl'].round(4)
mean_sim['cl'] = pd.to_numeric(mean_sim['cl'])
mean_sim_filtered = mean_sim[mean_sim['Points'] != 0]
SMALL_SIZE = 12
MEDIUM_SIZE = 12
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.figure(figsize=(7,7))

plt.scatter(mean_sim_filtered['cl'], mean_sim_filtered['Points'], zorder=1, edgecolors=None, color='#d62728',alpha=0.8)

b, m = polyfit(mean_sim_filtered['cl'], mean_sim_filtered['Points'], 1)

plt.plot(mean_sim_filtered['cl'], b + m * mean_sim_filtered['cl'], '-',color='#1f77b4', alpha=0.8, markersize=200)
plt.yticks(ticks=[1, 2, 3, 4, 5, 6, 7, 8, 10, 12])



plt.ylabel('Voting Points')
plt.xlabel('Average language similarity')

#plt.title(label='Relationship Between Voting Points and General Language Similarity')
plt.grid()
plt.show()
