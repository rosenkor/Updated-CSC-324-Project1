import sys
import time

"""

Here is what an example of a full url looks like: https://www.courtlistener.com/api/rest/v3/dockets/?clusters__date_filed__gt=2019-01-01&clusters__id__gt=0&clusters__opinions__author_str%21=%27%27&clusters__opinions__id__gt=0&court=scotus&order_by=id
Here is our link: https://www.courtlistener.com/api/rest/v3/

For each endpoint, due to pagination, we will need to use id to get the next page of results by using the id of the last result on the previous page and using the id__gt filter and sort_by=id.

What we want to filter by: 
docket__court=scotus
id__gt=0
date_filed__gt=2019-01-01
sub_opinions__isnull=False
sub_opinions_author__isnull=False


From the clusters endpoint, we want to get the following fields:
case_name
date_filed
scdb_decision_direction
scdb_votes_majority
scdb_votes_minority

From the sub_opinions endpoint, we want to get the following fields:
plain_text
html
html_lawbox
html_columbia
html_anon_2020
xml_harvard
html_with_citations
opinions_cited

from the author endpoint, we want to get the following fields:

From political_affiliations list, the political_party 
name_first
name_middle
name_last
name_suffix
date_dob

Here is how the linkage works:
The clusters field in the dockets endpoint is a [] of cluster ids.
The sub_opinions field in the dockets endpoint is a [] of sub_opinion ids.
The docket field in the clusters endpoint is a docket id.
The cluster field in the sub_opinions endpoint is a cluster id.
The author field in the sub_opinions endpoint is an author id.

political_affiliations is a field in the author endpoint that has multiple attributes including political_party.
"""
import os

os.environ["R_HOME"] = "C:\\ProgramData\\anaconda3\\Lib\\R\\"


import requests
from bs4 import BeautifulSoup as beautifulsoup
import json
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from urllib.parse import urlencode

import requests
import pandas as pd
from urllib.parse import urlencode

import os

# use maybe anaconda version of R

# "C:\ProgramData\anaconda3\Lib\R\bin\x64\R.dll"


def get_sequences(ids):
    sequences = []
    current_sequence = [ids[0]] if ids else []

    for i in range(1, len(ids)):
        if ids[i] == ids[i - 1] + 1:
            current_sequence.append(ids[i])
        else:
            sequences.append(current_sequence)
            current_sequence = [ids[i]]

    if current_sequence:
        sequences.append(current_sequence)
    return sequences


url = "https://www.courtlistener.com/api/rest/v3/"
api_key = "163cea228fb27936988d579ed72fe787848e1866"


def get_data_from_clusters(api_key, url):
    url = url + "clusters/"
    headers = {"Authorization": f"Token {api_key}"}
    params = {
        "dockets__court": "scotus",
        "id__gt": 0,  # Start from the first ID
        "date_filed__gt": "2019-01-01",
        "sub_opinions__isnull": False,
        "sub_opinions_author__isnull": False,
        "order_by": "id",
        "fields": "id,case_name,date_filed,scdb_decision_direction,scdb_votes_majority,scdb_votes_minority,sub_opinions"
    }

    clusters_data = []
    while True:
        response = requests.get(
            url, headers=headers, params=urlencode(params, safe=",")
        )
        response.raise_for_status()
        data = response.json()
        for cluster in data["results"]:
            sub_opinions = cluster["sub_opinions"]
            cluster["sub_opinions"] = [
                int(sub_opinion.split("/")[-2]) for sub_opinion in sub_opinions
            ]
        clusters_data.extend(data["results"])
        if not data["next"]:
            break
        params["id__gt"] = data["results"][-1]["id"]
        time.sleep(1)  # Add a delay to avoid being banned
    return clusters_data


def get_data_from_sub_opinions(api_key, url, sub_opinions_ids):
    url = url + "opinions/"
    headers = {"Authorization": f"Token {api_key}"}
    opinions_data = []

    for sequence in sub_opinions_ids:
        params = {
            "id__gte": sequence[0],
            "id__lte": sequence[-1],
            "author__gte": 0,
            "order_by": "id",
            "fields": "plain_text,html,html_lawbox,html_columbia,html_anon_2020,xml_harvard,html_with_citations,opinions_cited,author_id,id,cluster_id",
        }
        while True:
            response = requests.get(
                url, headers=headers, params=urlencode(params, safe=",")
            )
            response.raise_for_status()
            data = response.json()
            opinions_data.extend(data["results"])
            if not data["next"]:
                break
            params["id__gt"] = data["results"][-1]["id"]
    return opinions_data


def get_data_from_authors(api_key, url, author_ids):
    url = url + "people/"
    headers = {"Authorization": f"Token {api_key}"}
    authors_data = []

    author_ids = [id for id in author_ids if id not in [None, "None"]]

    for author_id in author_ids:
        params = {
            "id": author_id,
            "fields": "political_affiliations,name_first,name_middle,name_last,name_suffix,date_dob,id",
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        authors_data.extend(data["results"])
    return pd.DataFrame(authors_data)


def merge_data(clusters_data, opinions_data, authors_data):
    if not clusters_data:
        return None
    clusters_data = pd.DataFrame(clusters_data)
    opinions_data = pd.DataFrame(opinions_data)
    authors_data = pd.DataFrame(authors_data)

    authors_data["political_party"] = authors_data["political_affiliations"].apply(
        lambda x: x[0]["political_party"] if x else None
    )
    authors_data = authors_data.drop(columns=["political_affiliations"])

    clusters_data = clusters_data.rename(columns={"id": "cluster_id"})
    opinions_data = opinions_data.rename(
        columns={"id": "opinion_id", "cluster_id": "cluster_id"}
    )
    # for every type of opinion format, we want to make it into readable text like we want to make the xml into readable text that doesn't have any tags
    # we want to make the html into readable text that doesn't have any tags
    # we want to make the html_lawbox into readable text that doesn't have any tags
    # we want to make the html_columbia into readable text that doesn't have any tags
    # we want to make the html_anon_2020 into readable text that doesn't have any tags
    # we want to make the xml_harvard into readable text that doesn't have any tags
    # we want to make the html_with_citations into readable text that doesn't have any tags
    # we want to make the plain_text into readable text that doesn't have any tags

    opinions_data["plain_text"] = opinions_data["plain_text"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )
    opinions_data["html"] = opinions_data["html"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )
    opinions_data["html_lawbox"] = opinions_data["html_lawbox"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )
    opinions_data["html_columbia"] = opinions_data["html_columbia"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )
    opinions_data["html_anon_2020"] = opinions_data["html_anon_2020"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )
    opinions_data["xml_harvard"] = opinions_data["xml_harvard"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )
    opinions_data["html_with_citations"] = opinions_data["html_with_citations"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )

    # for the sub_opinion opions, we want you to make a list of all of the opinions text by coalescing the plain_text, html, html_lawbox, html_columbia, html_anon_2020, xml_harvard, html_with_citations fields
    opinions_data["opinions_text"] = opinions_data[
        [
            "plain_text",
            "html",
            "html_lawbox",
            "html_columbia",
            "html_anon_2020",
            "xml_harvard",
            "html_with_citations",
        ]
    ].apply(lambda x: " ".join(x.dropna()), axis=1)

    authors_data = authors_data.rename(columns={"id": "author_id"})

    clusters_data = clusters_data.merge(opinions_data, on="cluster_id", how="left")
    clusters_data = clusters_data.merge(authors_data, on="author_id", how="left")

    return pd.DataFrame(clusters_data)


def get_data(api_key, url):
    clusters_data = get_data_from_clusters(api_key, url)

    if not clusters_data:
        print("No cluster data found.")
        return None

    sub_opinions_ids = [
        cluster["sub_opinions"] for cluster in clusters_data if cluster["sub_opinions"]
    ]
    sub_opinions_ids = sorted(set(sum(sub_opinions_ids, [])))
    sub_opinions_sequences = get_sequences(sub_opinions_ids)

    opinions_data = (
        get_data_from_sub_opinions(api_key, url, sub_opinions_sequences)
        if sub_opinions_sequences
        else []
    )

    author_ids = [
        opinion["author_id"] for opinion in opinions_data if "author_id" in opinion
    ]
    author_ids = sorted(set(author_ids))
    author_ids_sequences = get_sequences(author_ids)

    authors_data = (
        get_data_from_authors(api_key, url, author_ids_sequences)
        if author_ids_sequences
        else pd.DataFrame()
    )

    return merge_data(
        clusters_data, opinions_data, authors_data
    )  # Eventually, this should merge clusters_data, opinions_data, and authors_data


import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

pandas2ri.activate()


# Function to handle conversion of opinions_text
def convert_opinions_text(x):
    if isinstance(x, list):
        return robjects.vectors.StrVector(
            [str(item) if item is not None else "None" for item in x]
        )
    return None


# Function to handle conversion of opinions_cited
def convert_opinions_cited(x):
    if isinstance(x, list):
        return robjects.vectors.StrVector(
            [str(item) if item is not None else "None" for item in x]
        )
    return None


def convert_sub_opinions(x):
    if isinstance(x, list):
        return robjects.vectors.StrVector(
            [str(item) if item is not None else "None" for item in x]
        )
    return None


def create_full_name(first_name, middle_name, last_name, suffix):
    name_parts = [first_name, middle_name, last_name, suffix]
    print(name_parts)
    # Filter out empty parts and join them with a space and remember about the NaNs and the ''s
    full_name = " ".join(
        [part for part in name_parts if part not in [np.nan, None, "None", ""]]
    )
    print(full_name)
    return full_name


def main():
    data = get_data(api_key, url)
    # We can have empty first name, an empty middle name, an empty last name, an empty suffix, and an empty date of birth
    # For example if we have only a first name, there should be no spaces in the full name
    # If we have a first name and a last name, there should be a space between the first and last name
    # If we have a first name, a middle name, and a last name, there should be a space between the first and middle name and a space between the middle and last names
    # If we have a first name, a middle name, a last name, and a suffix, there should be a space between the first and middle name, a space between the middle and last name, and a space between the last name and the suffix
    data["full_name"] = data.apply(
        lambda x: create_full_name(
            x["name_first"], x["name_middle"], x["name_last"], x["name_suffix"]
        ),
        axis=1,
    )
    data = data.drop(columns=["name_first", "name_middle", "name_last", "name_suffix"])

    # convert the data into an R object and export it as an RData file
    def replace_nan_with_none(x):
        if isinstance(x, list):
            return [item if pd.notna(item) else None for item in x]
        return None if pd.isna(x) else x

    columns_to_fix = [
        "plain_text",
        "html_with_citations",
        "html_anon_2020",
        "html_columbia",
        "html_lawbox",
        "html",
        "xml_harvard",
        "date_dob",
        "political_party",
    ]

    for col in columns_to_fix:
        data[col] = data[col].apply(replace_nan_with_none)

    # remember opinions_text could be a list of strings, a list of strings and none, or nothing and we are using pandas dataframe rn so if it is none it is NaN

    data["opinions_text"] = data["opinions_text"].apply(convert_opinions_text)
    data["opinions_cited"] = data["opinions_cited"].apply(convert_opinions_cited)
    data["sub_opinions"] = data["sub_opinions"].apply(convert_sub_opinions)

    # Fix sub_opinions
    data["sub_opinions"] = data["sub_opinions"].apply(convert_sub_opinions)
    data["opinions_cited"] = data["opinions_cited"].apply(convert_opinions_cited)

    r_data = pandas2ri.py2rpy(data)
    robjects.r.assign("data", r_data)
    robjects.r("save(data, file='data.RData')")


if __name__ == "__main__":
    main()
