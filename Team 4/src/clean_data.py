import numpy as np
import pandas as pd

# make sure its in English
 # could use spaCy, want to avoid having to hit an api, or downloading too much
 # maybe have that as an integration test?


def clean_bookend_quotes(string:str) -> str:
    """take out starting and ending quotes."""

    if string.startswith("'") and string.endswith("'"):
        string = string[-1:1]
    
    elif string.startswith('"') and string.endswith('"'):
        string = string[-1:1]

    return string


def clean_news(df:pd.DataFrame) -> pd.DataFrame:
    """Clean the News Series.
    
    using strip, to strip the start and end of the string.
    # TODO: should also check encoding
    """

    strings_ = []
    nan_cnt, byte_cnt = 0,0

    for news_string in df["News"].values:

        if news_string is np.nan:
            strings_.append("")
            nan_cnt += 1
            continue 
        
        if news_string.startswith("b"):
            cleaned_string = clean_bookend_quotes(news_string[1:].strip())
            strings_.append(cleaned_string) 
            byte_cnt += 1

        else:
            cleaned_string = clean_bookend_quotes(news_string.strip())
            strings_.append(cleaned_string)

    print(f"of {df.shape}, byte prefixes {byte_cnt} - filled in nans {nan_cnt}")
    df = df.assign(News=strings_)
    return df
 
