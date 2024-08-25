import json
import os
import glob
import pandas as pd

def handle_datetime_columns(df):
    """
    Converts datetime columns in a DataFrame to local time zone.

    Args:
        df (pandas.DataFrame): The DataFrame containing datetime columns.

    Returns:
        pandas.DataFrame: The DataFrame with datetime columns converted to local time zone.
    """
    for col in df.columns:
        if isinstance(df[col].dtype, pd.DatetimeTZDtype):
            df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
    return df


def prepare_arxiv_df():
    """
    Prepares the arXiv DataFrame by filtering and transforming the data.

    Returns:
        pandas.DataFrame: The prepared arXiv DataFrame.
    """
    # Set columns of interest
    cols = ['id', 'title', 'abstract', 'categories', 'doi', 'created', 'created_year', 'updated', 'authors']
    
    # Initialize data list
    data = []
    
    # Load arXiv data
    file_name = './arxiv/data/arxiv-metadata-oai-snapshot.json'
    file_path = os.path.dirname(file_name)
    
    # Print the location where the file is being searched
    print(f"Searching for the file in: {os.path.abspath(file_path)}")
    
    # List files in the directory
    files_in_directory = glob.glob(os.path.join(file_path, '*'))
    print(f"Files found in the directory: {files_in_directory}")

    try:
        with open(file_name, encoding='latin-1') as f:
            for i, line in enumerate(f):
                doc = json.loads(line)
                
                # Filter out papers that are not in the cs.CL category (Computation and Language)
                # Uncomment the following lines if you want to filter by category
                # if 'cs' not in doc['categories']:
                #     continue
                
                # Filter for time frame 2018-2024
                doc['created'] = doc['versions'][0]['created']
                doc['created_year'] = int(doc['created'].split(' ')[3])
                if doc['created_year'] < 2018:
                    continue
                
                # Perform query
                abstract = doc['abstract'].lower()
                if not ('transformer' in abstract or 'language model' in abstract or 'llms' in abstract):
                    continue
                if not ('knowledge' in abstract or 'context' in abstract or 'fact' in abstract):
                    continue
                if not ('conflict' in abstract or 'contradict' in abstract or 'inconsist' in abstract or 'counterfact' in abstract):
                    continue
                if not ('attention' in abstract or 'neuron' in abstract or 'feed-forward' in abstract or 'inner represent' in abstract or 'mechanistic interpret' in abstract or 'inner function' in abstract or 'causal analysis' in abstract or 'causal mediation' in abstract):
                    continue
                            
                lst = [doc['id'], doc['title'], doc['abstract'], doc['categories'], doc['doi'], doc['created'], doc['created_year'], doc['update_date'], doc['authors']]
                data.append(lst)

        arxiv_df = pd.DataFrame(data=data, columns=cols)

        arxiv_df = handle_datetime_columns(arxiv_df)

        return arxiv_df

    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found. Please make sure to provide it. Empty df was retruned.")
        return pd.DataFrame(columns=cols) 


def save_arxiv_df(arxiv_df):
    """
    Saves the arXiv DataFrame to Excel and Pickle formats.

    Args:
        arxiv_df (pandas.DataFrame): The arXiv DataFrame to be saved.
    """
    # Dataframe to Excel
    arxiv_df.to_excel("./arxiv/out/arxiv_df.xlsx")

    # Safe Dataframe to Pickle
    arxiv_df.to_pickle("./arxiv/out/arxiv_df.pkl")


if __name__ == "__main__":
    arxiv_df = prepare_arxiv_df()

    # Debug
    # arxiv_df.head()
    # arxiv_df.shape

    save_arxiv_df(arxiv_df)
