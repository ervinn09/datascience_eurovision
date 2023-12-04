import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import seaborn as sb

#init year
year = 2018
#years = [year := 2008, year := 2009,year := 2010]
#14  19
#list of countries that participated in ESC at least once
countries = [
    "Albania", "Andorra", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Cyprus",
    "Czechia", "Denmark", "Estonia", "Finland", "France", "Georgia", "Germany",
    "Greece", "Hungary", "Iceland", "Ireland", "Israel", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Morocco", "Netherlands",
    "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino",
    "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Turkey",
    "Ukraine", "United Kingdom", "Yugoslavia"
]

#converting to dataframes
ex = pd.read_csv("C:/Users/admin\project\eurovision\data\V-Dem-CY-Core-v13.csv")
votings = pd.read_excel("C:/Users/admin\project\eurovision\data\eurovision_song_contest_1975_2019.xlsx")
#make sure to run these commands first 'pip install openpyxl' and 'conda install openpyxl'

df_votings = pd.DataFrame(data = votings)

#remove duplicates
df_votings = df_votings[df_votings['Duplicate'] != 'x']

#renaming of countries
df_votings['To country'] =df_votings['To country'].replace('F.Y.R. Macedonia','North Macedonia')
df_votings['From country'] =df_votings['From country'].replace('F.Y.R. Macedonia','North Macedonia')
df_votings['To country'] =df_votings['To country'].replace('Bosnia & Herzegovina','Bosnia and Herzegovina')
df_votings['From country'] =df_votings['From country'].replace('Bosnia & Herzegovina','Bosnia and Herzegovina')

#filter only final and 2019 
#df_votings = df_votings.groupby(df_votings['Year'])
#df_votings = df_votings.get_group(year)
df_votings = df_votings.groupby(df_votings['(semi-) final'])
df_votings = df_votings.get_group('f')
#df_votings = df_votings.groupby(df_votings['Jury or Televoting'])
#df_votings = df_votings.get_group('J')

#remove 0 points
df_votings = df_votings[df_votings['Points      '] != 0]

#df_votings = df_votings.groupby(df_votings['From country'])
#df_votings = df_votings.get_group('Belgium')




#keeping only columns about democracy index
ex = pd.DataFrame(data = ex)
a = ['country_name','year','v2x_polyarchy','v2x_libdem','v2x_partipdem','v2x_delibdem','v2x_egaldem']
ex1 = ex.loc[:, a]

#keeping the years from 1956 only since Eurovision started at 1956
start_year = 1975
end_year = 2019
ex_filtered = ex1[(ex1['year'] >= start_year) & (ex1['year'] <= end_year) ]
ex_filtered = ex_filtered.rename(columns={'year': 'Year'})



# Filter the DataFrame to include only the countries in the list
ex_filtered = ex_filtered[ex_filtered['country_name'].isin(countries)]
#print(ex_filtered)

#only countries participated in Eurovision
grouped = ex_filtered.groupby('country_name')
unique_countries = grouped.groups.keys()


#ex_filtered.to_csv('test.csv', index = False)

#calculates one democracy index by adding all other indexes and dividing them with the number of indexes


ex_filtered['dem_index'] = (ex_filtered['v2x_polyarchy']+ex_filtered['v2x_libdem']+
             ex_filtered['v2x_partipdem']+ex_filtered['v2x_delibdem']+ex_filtered['v2x_egaldem'])/5

#ex_filtered['country_name'] = ex_filtered.groupby('country_name')
ex_filtered['country_name'] = ex_filtered['country_name'].replace('Netherlands','The Netherlands')
ex_filtered['country_name'] = ex_filtered['country_name'].replace('Czechia','Czech Republic')
#ex_filtered.to_csv('test1.csv',index = False)

#ex_filtered_year_2019 = ex_filtered.groupby(ex_filtered['year'])
#ex_filtered_year_2019 = ex_filtered_year_2019.get_group(year)



#plot
#sb.barplot(ex_filtered_year_2019,y='dem_index',x='country_name',color= 'blue' )
#sb.despine()
#mp.xticks(rotation = -90,fontsize = 7)
#mp.gca().set_xticklabels(mp.gca().get_xticklabels())

#mp.xlabel('Counties')
#mp.ylabel('Democracy index for 2019')
#mp.show()



exm =  ex_filtered.rename(columns = {'country_name': 'To country'})
exm = exm.drop(['v2x_polyarchy','v2x_libdem','v2x_partipdem','v2x_delibdem','v2x_egaldem'], axis = 1)
average_dem_index = exm['dem_index'].mean()

# Create a DataFrame with the new row
new_row_df = pd.DataFrame({'To country': ['San Marino'], 'dem_index': [average_dem_index]})

# Concatenate the original DataFrame 'exm' with the new DataFrame 'new_row_df'
exm = pd.concat([exm, new_row_df], ignore_index=True)
exm.to_csv('sefea.csv',index=False)


merged_df = pd.merge(df_votings, exm, on=['To country','Year'], how='left')

merged_df['dem_index'] = merged_df['dem_index']
#print(merged_df)

#multiply coeff with points

merged_df['coeff'] = merged_df['dem_index'] * merged_df['Points      ']
#merged_df = merged_df.groupby(merged_df['To country'])
#merged_df = sum(merged_df['coeff'])
merged_df['coeff'] = merged_df['coeff'].map(lambda x: round(x, 3))
#dem index column
#dem_df = merged_df.drop(['coeff','From country','(semi-) final','Jury or Televoting','Points      ','Duplicate','Edition','Year'],axis=1)
#dem_df = dem_df.drop_duplicates()


#order countries asc dem_index
ord_df = merged_df.drop(['(semi-) final','Jury or Televoting','Points      ','Duplicate','Edition'],axis=1)
print(ord_df)
ord_df.to_csv('teswwwt233.csv', index = False)

#ord_df = ord_df.groupby(['Year_x','From country'])
#ord_df = ord_df['coeff'].sum().reset_index()
ord_df = ord_df.pivot_table(index=['From country', 'Year'], values='coeff', aggfunc='sum').reset_index()

print(ord_df)    
#print(ord_df['From country'].unique())
#ord_df = ord_df.drop_duplicates()
#rename of column for merge : is actually to !!! not From
exm = exm.rename(columns={'To country': 'From country'})

#print(sum(merged_df['coeff']))
merged_df.to_csv('test3.csv', index = False)
#test = merged_df.drop(['(semi-) final','Jury or Televoting','Points      ','Duplicate','Edition','Year'],axis=1)
#print(test)
#test = test.groupby('From country')['coeff'].sum().reset_index()
#test['coeff'] = (test['coeff'] - test['coeff'].min()) / (test['coeff'].max() - test['coeff'].min())
#print(test)


test = pd.merge(exm,ord_df,on=['From country','Year'], how='left')
test = test.sort_values(by='dem_index', ascending=True)
test = test.dropna(subset=['coeff'])
test['firstcol'] = test.apply(lambda row: f"{row['From country']} ({str(row['dem_index'])[:4]})", axis=1)
# Remove rows where Country is "San Marino"
test = test[test['From country'] != 'San Marino']

#filter years
years_to_filter = [2001,1999,2019,2014]
test2 = test[test['Year'].isin(years_to_filter)]

#remove .0 
test2['Year'] = test2['Year'].astype(int)

highlight_index = [13,20,30]

#mp.xlim(20,60)  # Set the x-axis limits


#ax.grid(True, linestyle='--', linewidth=0.5)
#ax.set_xticks([0, 1, 2, 3, 4])
#ax.set_yticks([0, 10, 20, 30, 40])

#Azerbaijan example
#custom_palette = {'low': 'blue', 'high': 'red'}#

#corr coeff
test1 = test.groupby('Year')['coeff'].corr(test['dem_index']).reset_index()
test1 = test1.rename(columns = {'coeff':'Correlation coeff'})
test = pd.merge(test, test1, on= 'Year')
#sb.set(style="whitegrid")


g = sb.FacetGrid(test2, col='Year', col_wrap=2, height=6)
#test['coeff'] = test['coeff'].astype(int)
g.map_dataframe(sb.regplot, x='dem_index', y='coeff', color = 'steelblue' )
#sb.regplot(test, x = 'dem_index', y= 'coeff', color = 'blue' )
#mp.plot(test,x = 'coeff', y= 'firstcol', marker='o', color='red')
#mp.scatter(test['coeff'], test['firstcol'], color='blue', marker='o')
g.set_axis_labels('Democracy Index', 'Weighted Points')
g.set_titles('Year {col_name}')

mp.legend()
# Adjust the spacing between subplots
mp.tight_layout()

#mp.set_ylabel('Weighted Points', fontsize=14,fontweight ='bold')
#mp.set_xlabel('Democracy index',fontsize=14,fontweight ='bold')
#ax.set_title('Given votes of countries in relation with democracy index ',fontsize=20,fontweight ='bold')

# Highlight the bars
#for index in highlight_index:
#    ax.patches[index].set_hatch('///')  # Set patterned hatching for the highlighted bars

# Set the color for all bars
#for patch in ax.patches:
#    patch.set_facecolor('blue')


#g.xticks(fontsize = 7)
#g.yticks(fontsize = 7)
#g.gca().set_xticklabels(mp.gca().get_xticklabels())
#g.tick_params( labelsize=12)



# Calculate correlation coefficient
#correlation = np.corrcoef(test['dem_index'], test['coeff'])[0, 1]

# Calculate line equation
#slope = correlation * np.std(test['coeff']) / np.std(test['dem_index'])
#intercept = np.mean(test['coeff']) - slope * np.mean(test['dem_index'])

# Plot correlation line
#mp.plot(test['dem_index'], slope * test['dem_index'] + intercept, color='red')

sb.despine()

mp.grid(False)

mp.show()

#fig1 = mp.figure(figsize=[9,7])

#sb.factorplot("coeff", "firstcol", col=[year := 2002,year := 2004], data=test, kind="bar")
correlation_coefficient = test['coeff'].corr(test['dem_index'])
print("Correlation Coefficient of year", year , " :",+ round(correlation_coefficient,2))

# Create a line plot
mp.figure(figsize=(12, 9))
sb.lineplot(x='Year', y='Correlation coeff', data=test1, marker='o', color='steelblue')
mp.xlabel('Year', fontsize=14)
mp.ylabel('Correlation Coefficient', fontsize=14)
#mp.title('Correlation Coefficient Over Years')
mp.grid(True)
mp.show()



#mp.xticks(rotation = -90,fontsize = 7)
#mp.gca().set_xticklabels(mp.gca().get_xticklabels())
