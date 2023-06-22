import matplotlib.pyplot as plt
import seaborn as sns


def display(choice,data):
    """
    Plots the data (written to reduce the lines in main code)
    :param choice: choice of parameter to display Country/Shakha
    :param data: original dataset from xlsx
    :return: none
    """
    distance = data.groupby(choice)['Distance (in Km)'].sum().sort_values(ascending=False)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=distance.values, y=distance.index, estimator=sum, errorbar=None)

    for bar in plt.gca().patches:
        plt.gca().annotate(f"{bar.get_width():.0f}", (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                           ha='left', va='center', xytext=(5, 0), textcoords='offset points')

    plt.xlabel('Total Distance (in Km)')
    plt.ylabel(f'{choice}')
    plt.title(f'Total distance by {choice}')
    plt.savefig(f'total_distance_by_{choice}.png', bbox_inches='tight')


def display_top_five(choice, data):
    """
    To display top 5 countries/shakhas
    :param choice: choice of parameter to display Country/Shakha
    :param data: original dataset from xlsx
    :return: None
    """
    top_countries = data.groupby(choice)['Distance (in Km)'].sum().nlargest(5).index.tolist()
    top_countries_data = data[data[choice].isin(top_countries)]

    # Generate plots for top five countries
    plt.figure(figsize=(12, 6))
    country_distance = top_countries_data.groupby(choice)['Distance (in Km)'].sum().sort_values(ascending=False)
    sns.barplot(x=country_distance.values, y=country_distance.index, estimator=sum, errorbar=None)

    for bar in plt.gca().patches:
        plt.gca().annotate(f"{bar.get_width():.0f}", (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                           ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    plt.xlabel(f'{choice}')
    plt.ylabel('Total Distance (in Km)')
    plt.title(f'Total distance covered by Top 5 {choice}')
    plt.savefig(f'total_distance_by_top_{choice}.png', bbox_inches='tight')