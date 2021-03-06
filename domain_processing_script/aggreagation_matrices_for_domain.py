from helper_methods import get_column_names_for_simple_matrix_dictionary
from datetime import datetime
import pandas as pd

# import os
# os.chdir(os.getcwd() + '/domain_processing_script')

def create_simple_aggregate_matrix_for(month, variable_name, ratio):
    column_name = get_column_names_for_simple_matrix_dictionary().get(variable_name)
    source_path = 'resources/source_data/cleaner_data_' + month + '.csv'
    data = pd.read_csv(source_path).dropna(subset=['Obsah zmínek'])
    data.sort_values(by='Datum vytvoření', inplace=True)
    train_set_size = int(len(data) * ratio)
    data = data[:train_set_size]
    data = data[[column_name, 'Štítek']]
    value_counts = data[column_name].value_counts()
    values = value_counts.keys()
    temp = list([])
    for value in values:
        row = dict({})
        value_data = data.loc[data[column_name] == value]['Štítek']
        row[variable_name] = value
        row[variable_name + '_count'] = len(value_data)
        row[variable_name + '_count_rel'] = len(value_data.loc[value_data == 'rel'])
        row[variable_name + '_count_nerel'] = len(value_data.loc[value_data == 'nerel'])
        temp.append(row)
    aggregate_matrix = pd.DataFrame(data=temp)[[variable_name, variable_name + '_count', variable_name + '_count_rel', variable_name + '_count_nerel']]
    return aggregate_matrix


def create_aggregation_matrices_for_domain_and_domain_group(month, ratio=1.0):
    time = datetime.now().strftime('%c').replace(' ', '_')
    aggregate_matrix_domain = create_simple_aggregate_matrix_for(month, 'domain', ratio)
    aggregate_matrix_domaingroup = create_simple_aggregate_matrix_for(month, 'domaingroup', ratio)
    path_domain = 'resources/aggregation_matrices/domain/' + month + '/'
    path_domaingroup = 'resources/aggregation_matrices/domain_group/' + month + '/'
    aggregate_matrix_domain.to_csv(path_domain + 'latest.csv')
    aggregate_matrix_domain.to_csv(path_domain + time + '.csv')
    aggregate_matrix_domaingroup.to_csv(path_domaingroup + 'latest.csv')
    aggregate_matrix_domaingroup.to_csv(path_domaingroup + time + '.csv')


# create_aggregation_matrices_for_domain_and_domain_group('prosinec', 0.70)