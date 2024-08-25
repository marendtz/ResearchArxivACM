import pandas as pd

def load_dataframes():
    """
    Load arxiv_df and acm_df from Excel files.
    Returns:
        arxiv_df (pandas.DataFrame): Arxiv dataframe.
        acm_df (pandas.DataFrame): ACM dataframe.
    """
    arxiv_df = pd.read_excel('./analysis/in/arxiv_df.xlsx')
    acm_df = pd.read_excel('./analysis/in/acm_df.xlsx')
    return arxiv_df, acm_df

def select_columns_rename(arxiv_df, acm_df):
    """
    Select desired columns from each dataframe and rename them.
    Args:
        arxiv_df (pandas.DataFrame): Arxiv dataframe.
        acm_df (pandas.DataFrame): ACM dataframe.
    Returns:
        arxiv_selected (pandas.DataFrame): Selected and renamed columns from arxiv_df.
        acm_selected (pandas.DataFrame): Selected and renamed columns from acm_df.
    """
    arxiv_selected = arxiv_df[['title', 'abstract', 'authors', 'created_year']]
    arxiv_selected.rename(columns={'created_year': 'year'}, inplace=True)
    arxiv_selected['source'] = 'arxiv'

    acm_selected = acm_df[['Title', 'Abstract', 'Authors', 'Date published']]
    acm_selected.rename(columns={'Title': 'title', 'Authors': 'authors', 'Date published': 'year'}, inplace=True)
    acm_selected["year"] = acm_selected["year"].astype(str).str.split('-').str[0].astype(int)
    acm_selected.rename(columns={'Abstract': 'abstract'}, inplace=True)
    acm_selected['source'] = 'acm'

    return arxiv_selected, acm_selected

def merge_dataframes(arxiv_selected, acm_selected):
    """
    Merge the selected dataframes.
    Args:
        arxiv_selected (pandas.DataFrame): Selected and renamed columns from arxiv_df.
        acm_selected (pandas.DataFrame): Selected and renamed columns from acm_df.
    Returns:
        merged_df (pandas.DataFrame): Merged dataframe.
    """
    merged_df = pd.concat([arxiv_selected, acm_selected])
    merged_df.reset_index(drop=True, inplace=True)
    return merged_df

def remove_duplicates(merged_df):
    """
    Remove duplicates from the merged dataframe based on the 'title' column.
    Args:
        merged_df (pandas.DataFrame): Merged dataframe.
    Returns:
        merged_df (pandas.DataFrame): Merged dataframe without duplicates.
    """
    merged_df['title_check'] = merged_df['title'].astype(str).str.lower().replace(' ','').replace('[^a-z0-9]', '', regex=True)
    merged_df.drop_duplicates(subset='title_check', keep='first', inplace=True)
    merged_df.drop(columns=['title_check'], inplace=True)
    merged_df.reset_index(drop=True, inplace=True)
    return merged_df

def save_dataframes(merged_df):
    """
    Save the merged dataframe to Excel and pickle files.
    Args:
        merged_df (pandas.DataFrame): Merged dataframe.
    """
    merged_df.to_excel("./analysis/intermediate/merged_df.xlsx")
    merged_df.to_pickle("./analysis/intermediate/merged_df.pkl")

# Main execution
if __name__ == "__main__":
    arxiv_df, acm_df = load_dataframes()
    arxiv_selected, acm_selected = select_columns_rename(arxiv_df, acm_df)
    merged_df = merge_dataframes(arxiv_selected, acm_selected)
    merged_df = remove_duplicates(merged_df)
    save_dataframes(merged_df)




