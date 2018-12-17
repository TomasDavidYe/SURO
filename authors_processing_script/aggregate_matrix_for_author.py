import numpy as np
from helper_methods import *
from datetime import datetime


def get_features_for_author(author, dataset):
    result = {}
    author_data = dataset.loc[dataset['Autor'] == author].copy()
    result['author'] = author
    result['author_count_total'] = len(author_data)
    result['author_count_rel'] = len(author_data.loc[author_data['Štítek'] == 'rel'])
    result['author_count_nerel'] = len(author_data.loc[author_data['Štítek'] == 'nerel'])
    author_data.drop(columns=['Autor', 'Štítek'], inplace=True)
    averages = author_data.apply(np.average)
    for column_name in author_data.columns.values:
        result['author_avg_' + column_name] = averages[column_name]
    return result

def reorder_columns(matrix):
    temp = matrix.columns.values.tolist()[1:-3]
    temp.remove('author_avg_followers')
    temp.remove('author_avg_fans')
    temp.remove('author_avg_favs')
    temp.remove('author_avg_influenceScore')
    cols = ['author',
            'author_count_total',
            'author_count_rel',
            'author_count_nerel',
            'author_avg_influenceScore',
            'author_avg_followers',
            'author_avg_fans',
            'author_avg_favs'] + temp
    return matrix[cols]


def create_aggregation_matrix_author(ratio=1.0):
    column_names_for_dropping = get_column_names_for_dropping()
    dataset = pd.read_csv('../resources/general_data/cleaner_data.csv').dropna(subset=['Autor']).drop(
        columns=column_names_for_dropping).fillna(0)
    train_set_size = int(len(dataset) * ratio)
    dataset = dataset[:train_set_size]
    authors_column = dataset['Autor']
    value_counts = authors_column.value_counts()
    authors = value_counts.keys()
    temp = []
    for author in authors:
        temp.append(get_features_for_author(author, dataset))
    aggregate_matrix_authors = pd.DataFrame(temp)

    aggregate_matrix_authors = reorder_columns(aggregate_matrix_authors)
    time = datetime.now().strftime('%c').replace(' ', '_')
    aggregate_matrix_authors.to_csv('../resources/aggregation_matrices/authors/aggregation_matrix_authors_' + time + '.csv')


create_aggregation_matrix_author(0.8)



