import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np


def restaurant_business_exploration(file):

    #Credit: https://www.reddit.com/r/MachineLearning/comments/33eglq/python_help_jsoncsv_pandas/
    # read the entire file into a python array
    with open(file, 'rb') as f:
        business_data = f.readlines()
    print('Data loaded')

    # remove the trailing "\n" from each line
    business_data = map(lambda x: x.rstrip(), business_data)
    business_data_json_str = b"[" + b','.join(business_data) + b"]"
    business_data_df = pd.read_json(business_data_json_str)
    print('json converted to dataframe')

    tokenized_cols_business = business_data_df.categories.str.split(',', expand=True)
    tokenized_cols_business = tokenized_cols_business.rename(columns=lambda x: str(x)+'_category')
    print('Categories column split by list info')

    merged_business_data = pd.merge(business_data_df, tokenized_cols_business, left_index=True, right_index=True)
    merged_business_data = merged_business_data[merged_business_data.apply(lambda r: r.str.contains('Restaurants', case=False).any(), axis=1)]
    print('Tokenized categories with Restaurant in its row merged with original data')

    merged_business_data.to_csv('businesses_with_restaurants_tag_new_correct.csv')
    print('Tokenized data written to csv')

    categories = merged_business_data.iloc[:,14:51]
    categories.head()

    test_categories = categories
    threshold = 200 # Anything that occurs less than this will be removed.
    value_counts = test_categories.stack().value_counts() # Entire DataFrame
    to_remove = value_counts[value_counts <= threshold].index
    test_categories.replace(to_remove, 'None', inplace=True)
    print('Non-pertinent categories removed based on 200 count threshold')

    merged_clean_business_data = pd.merge(business_data_df, test_categories, left_index=True, right_index=True)
    print('Clean categories merged back with original data')

    merged_business_data.to_csv('clean_file_restaurants_with_pertinent_categories.csv')
    print("Done!")


def main():

    restaurant_business_exploration('../data/yelp_academic_dataset_business.json')

main()