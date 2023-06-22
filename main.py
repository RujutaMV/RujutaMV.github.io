"""
Important :
    Before running this code, change the name column in xlsx and rename Associated Shakha (Optional) to Associated Shakha

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
from function import display, display_top_five

data = pd.read_excel('VDM_080623.xlsx')      # Read the Excel dataset
plt.rcParams.update({'font.size': 20})
TopNnumbers = 5

# Clean the data
data['Date of the activity'] = pd.to_datetime(data['Date of the activity']).dt.date  # Extract date only
data = data[data['Date of the activity'] >= pd.to_datetime(
    '2023-05-15').date()]  # Filter out rows with date before 15th May 2023
sns.set(style="whitegrid")

display('Country', data)       # function call to display Total distance by Country

data['Associated Shakha'] = data['Associated Shakha'].fillna('Not associated')
display('Associated Shakha', data)     # function call to display Total distance by Associated Shakha

# Daily distance sum by Sports type
plt.figure(figsize=(12, 6))
sns.barplot(data=data, x='Date of the activity', y='Distance (in Km)', hue='Sports Type', estimator=sum, errorbar=None)
for bar in plt.gca().patches:
    plt.gca().annotate(f"{bar.get_height():.0f}", (bar.get_x() + bar.get_width() / 2, bar.get_height()), ha='center',
                       va='center', xytext=(0, 5), textcoords='offset points')
plt.xlabel('Date')
plt.ylabel('Distance (in Km)')
plt.title('Daily distance sum by Sports type')
plt.xticks(rotation=45)
plt.legend(loc='upper right')
plt.savefig('daily_distance_by_sports.png', bbox_inches='tight')


display_top_five('Name', data)          # Filter top five Names based on distance

display_top_five('Country', data)       # Filter top five countries based on distance

display_top_five('Associated Shakha', data)     # Filter top five Associated Shakha based on distance

# Calculate the sum of distances for each activity
# activity_distances = data.groupby('Sports Type')['Distance (in Km)'].sum().reset_index()

# Filter the top five names based on total distance for each activity
top_names_by_activity = data.groupby(['Sports Type', 'Name'])['Distance (in Km)'].sum().groupby('Sports Type',
                                                                                                group_keys=False).nlargest(
    TopNnumbers).reset_index()

# Plot top five Names and their distances, separated by activity
plt.figure(figsize=(14, 6))
sns.barplot(data=top_names_by_activity, x='Distance (in Km)', y='Name', hue='Sports Type', orient='h')

plt.legend()
plt.title('Top five Names and their distances by activity')
plt.savefig('top_five_names_by_activity.png', bbox_inches='tight')

# Show all plots
# plt.show()

# Plot 5: Distance covered by activity as a pie chart
# activity_distance = data.groupby('Sports Type')['Distance (in Km)'].sum()
# plt.pie(activity_distance, labels=activity_distance.index, autopct='%1.1f%%', startangle=90)
# plt.title('Distance covered by activity')

# Add total distance and percentage covered annotations
# total_distance = round(activity_distance.sum())

# Plot top five Names by distance, separate plot for each activity (daily)
today = datetime.date.today() - timedelta(days=1)       # =0 for today, =1 for yesterday!
today_data = data[data['Date of the activity'] == today]

data = data.rename(columns={"Option 2": "Timestamp"})

# Filter data by today's entries based on the Timestamp column
today_entries = data[pd.to_datetime(data['Timestamp']).dt.date == today]

# Plot 6: Distance covered by age as a pie chart for today's entries
age_distance_today = round(today_entries.groupby('Age ')['Distance (in Km)'].sum())

# Add total distance and percentage covered annotations
total_distance_today = round(age_distance_today.sum())

# Plot 7: Distance covered by age as a pie chart for all dates until now
plt.figure(figsize=(10, 8))
age_distance_all = data.groupby('Age ')['Distance (in Km)'].sum()
# plt.pie(age_distance_all, labels=age_distance_all.index)#, autopct='%1.1f%%', startangle=90)
plt.title(f'Distance covered by age till {today}')

# Add total distance and percentage covered annotations
total_distance_all = round(age_distance_all.sum())
plt.annotate(f'Total Distance: {total_distance_all} km', xy=(0.5, 0.5), xytext=(0, 0), ha='center', va='center',
             fontsize=16)

# Calculate percentage covered for each age group
percentage_covered_all = (age_distance_all / total_distance_all) * 100

# Generate the donut plot with bright color scheme
colors = sns.color_palette('bright', len(age_distance_all))
plt.pie(age_distance_all, labels=age_distance_all.index, colors=colors)  # , autopct='%1.1f%%', startangle=90)

# Draw a white circle at the center to create a donut chart
center_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(center_circle)

# Add total distance and percentage covered annotations
# plt.text(0, 0, f'Total Distance: {total_distance_today} km', ha='center', va='center', fontsize=12)
for i, (age, distance) in enumerate(age_distance_all.items()):
    plt.text(0, -0.1 - i * 0.1, f'Age {age}: {distance} km ({percentage_covered_all[i]:.1f}%)', ha='center',
             va='center', fontsize=14)

plt.title(f'Distance covered by age {today}')
plt.axis('equal')
plt.savefig(f'distance_by_age_{today}_donut_plot.png', bbox_inches='tight')

# CurrentTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

for activity in today_data['Sports Type'].unique():
    top_names_activity = today_data[today_data['Sports Type'] == activity].groupby('Name')[
        'Distance (in Km)'].sum().nlargest(TopNnumbers).index.tolist()
    plt.figure(figsize=(10, 5))
    sns.barplot(data=today_data[today_data['Name'].isin(top_names_activity) & (today_data['Sports Type'] == activity)],
                y='Name', x='Distance (in Km)', hue='Country',
                errorbar=None)

    for bar in plt.gca().patches:
        plt.gca().annotate(f"{bar.get_width():.0f}", (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                           ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    plt.title(f'Top 5 Names by Distance - {activity} - as on {today}')
    plt.savefig(f'top_5_names_by_distance_{activity}.png', bbox_inches='tight')

UniqueNames = data['Name'].unique()
UniqueIDCountries = data.groupby('Country')['Name'].nunique()

print("Unique Names Count ", len(UniqueNames))

# Calculate total distance by country
country_total_distance = data.groupby('Country')['Distance (in Km)'].sum()
total_distance = round(country_total_distance.sum())

# Create a donut plot
plt.figure(figsize=(8, 8))
sns.set_palette("bright")
w,l,p = plt.pie(country_total_distance, labels=country_total_distance.index,
        autopct='%1.1f%%', startangle=180, pctdistance=0.85, rotatelabels=True,
        wedgeprops=dict(width=0.3))
[t.set_rotation(315) for t in p]
plt.gca().add_artist(plt.Circle((0, 0), 0.6, fc='white'))  # Draw a white circle to create a donut chart

# Annotate the total distance at the center
plt.text(0, 0, f'Total Distance: {total_distance} km', ha='center', va='center', fontsize=15)

plt.title('Total Distance by Country (Donut Chart)')
plt.axis('equal')
plt.tight_layout()
# plt.xticks(rotation=45)
plt.savefig('total_distance_by_country_donut.png', bbox_inches='tight')

# Count of unique 'Name' by country
unique_name_count = data.groupby('Country')['Name'].nunique().sort_values(ascending=False)

# Create a bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x=unique_name_count.index, y=unique_name_count.values, palette='bright')
plt.xlabel('Country')
plt.ylabel('Unique Name Count')
plt.title('Unique Name Count by Country')
plt.xticks(rotation=45)

# Add value labels on top of each bar
for i, value in enumerate(unique_name_count.values):
    plt.text(i, value, str(value), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('unique_name_count_by_country.png', bbox_inches='tight')
