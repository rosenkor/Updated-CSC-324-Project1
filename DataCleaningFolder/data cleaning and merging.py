import pickle
import pandas as pd
from bs4 import BeautifulSoup as beautifulsoup


with open("C:\\Users\\Kory\\Downloads\\clusters_data.pickle", 'rb') as f:
    clusters_data = pickle.load(f)
with open("C:\\Users\\Kory\\Downloads\\opinions_data.pickle", 'rb') as f:
    opinions_data = pickle.load(f)
with open("C:\\Users\\Kory\\Downloads\\authors_data.pickle", 'rb') as f:
    authors_data = pickle.load(f)
with open("C:\\Users\\Kory\\Downloads\\docket_ids.pickle", 'rb') as f:
    dockets_ids = pickle.load(f)

clusters_data = pd.DataFrame(clusters_data)
opinions_data = pd.DataFrame(opinions_data)
authors_data = pd.DataFrame(authors_data)
dockets_ids = pd.DataFrame(dockets_ids)

dockets_ids = dockets_ids.rename(columns = {0: "cluster_id", 1: "docket_id"})
print(dockets_ids)

# remove the scdb_decision_direction as it is too hard to figure out manually
clusters_data = clusters_data.drop(columns=["scdb_decision_direction"])



authors_data = authors_data.rename(columns={"political_affiliation": "political_affiliations"})

print(authors_data["political_affiliations"][0])


# This person is not a supreme court justice and should be removed
authors_data = authors_data[authors_data["id"] != 8611]

authors_data["political_party"] = authors_data["political_affiliations"].apply(
    lambda x: x["political_party"] if x and "political_party" in x else None
)
authors_data["date_start"] = authors_data["political_affiliations"].apply(
    lambda x: x["date_start"] if x and "date_start" in x else None
)

authors_data["date_left"] = authors_data["political_affiliations"].apply(
    lambda x: x["date_left"] if x and "date_left" in x else None
)
authors_data = authors_data.drop(columns=["political_affiliations"])

# We have to edit some of the date_left for some of the justices

# For person with the id 1213, they left September 18, 2020

authors_data.loc[authors_data["id"] == 1213, "date_left"] = "2020-09-18"

# For person with the 384 , they left June 30, 2022

authors_data.loc[authors_data["id"] == 384, "date_left"] = "2022-06-30"


# Let's go fixing up the data for each justice

# For person with the id 77, they were born April 1, 1950, they started January 31, 2006

authors_data.loc[authors_data["id"] == 77, "date_dob"] = "1950-04-01"
authors_data.loc[authors_data["id"] == 77, "date_start"] = "2006-01-31"

# For the person with the id 384, they were born August 15, 1938, they started August 3, 1994

authors_data.loc[authors_data["id"] == 384, "date_dob"] = "1938-08-15"
authors_data.loc[authors_data["id"] == 384, "date_start"] = "1994-08-03"

# For the person with the id 1213, they were born March 15, 1933, they started August 10, 1993

authors_data.loc[authors_data["id"] == 1213, "date_dob"] = "1933-03-15"
authors_data.loc[authors_data["id"] == 1213, "date_start"] = "1993-08-10"

# For the person with the id 1250, they were born August 29, 1967, they started April 10, 2017

authors_data.loc[authors_data["id"] == 1250, "date_dob"] = "1967-08-29"
authors_data.loc[authors_data["id"] == 1250, "date_start"] = "2017-04-10"

# For the person with the id 1609, they were born September 14, 1970, they started June 30, 2022

authors_data.loc[authors_data["id"] == 1609, "date_dob"] = "1970-09-14"
authors_data.loc[authors_data["id"] == 1609, "date_start"] = "2022-06-30"

# For the person with the id 1691, they were born April 28, 1960, they started August 7, 2010

authors_data.loc[authors_data["id"] == 1691, "date_dob"] = "1960-04-28"
authors_data.loc[authors_data["id"] == 1691, "date_start"] = "2010-08-07"

# For the person with the id 1713, they were born February 12, 1965, they started October 6, 2018

authors_data.loc[authors_data["id"] == 1713, "date_dob"] = "1965-02-12"
authors_data.loc[authors_data["id"] == 1713, "date_start"] = "2018-10-06"

# For the person with the id 2738, they were born January 27, 1955, they started September 29, 2005

authors_data.loc[authors_data["id"] == 2738, "date_dob"] = "1955-01-27"
authors_data.loc[authors_data["id"] == 2738, "date_start"] = "2005-09-29"

# For the person with the id 3045, they were born June 25, 1954, they started August 8, 2009

authors_data.loc[authors_data["id"] == 3045, "date_dob"] = "1954-06-25"
authors_data.loc[authors_data["id"] == 3045, "date_start"] = "2009-08-08"

# For the person with the id 3200, they were born June 23, 1948, they started October 23, 1991

authors_data.loc[authors_data["id"] == 3200, "date_dob"] = "1948-06-23"
authors_data.loc[authors_data["id"] == 3200, "date_start"] = "1991-10-23"

# For the person with the id 8543, they were born January 28, 1972, they started October 27, 2020

authors_data.loc[authors_data["id"] == 8543, "date_dob"] = "1972-01-28"
authors_data.loc[authors_data["id"] == 8543, "date_start"] = "2020-10-27"




clusters_data = clusters_data.rename(columns={"id": "cluster_id"})
opinions_data = opinions_data.rename(
        columns={"id": "opinion_id", "cluster_id": "cluster_id"}
    )
authors_data = authors_data.rename(columns={"id": "author_id"})

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
        lambda x: beautifulsoup(x, features="xml").get_text() if x else None
    )
opinions_data["html_with_citations"] = opinions_data["html_with_citations"].apply(
        lambda x: beautifulsoup(x, "html.parser").get_text() if x else None
    )

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
].apply(lambda x: [text for text in x.dropna() if text], axis=1)

opinions_data = opinions_data.drop(
        columns=[
            "plain_text",
            "html",
            "html_lawbox",
            "html_columbia",
            "html_anon_2020",
            "xml_harvard",
            "html_with_citations",
        ]
    )

print(authors_data)

new_data = clusters_data.merge(opinions_data, on="cluster_id", how="left")
new_data = new_data.merge(authors_data, on="author_id", how="inner")
new_data = new_data.merge(dockets_ids, on="cluster_id", how="inner")

# Lets fix some more information

# Add a column for the Decision
new_data["decision"] = None


# Lets start with the case of Great Lakes Ins. SE v. Raiders Retreat Realty Co.
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 67868770, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67868770, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67868770, "decision"] = "reversed"

# Lets move on to Acheson Hotels, LLC v. Laufer
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0

new_data.loc[new_data["docket_id"] == 67855146, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67855146, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67855146, "decision"] = "vacated and remanded"

# Lets move on to Murray v. UBS Securities, LLC
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0

new_data.loc[new_data["docket_id"] == 67868053, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67868053, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67868053, "decision"] = "reversed and remanded"

# Lets move on to Department of Agriculture Rural Development Rural Housing Service v. Kirtz
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0

new_data.loc[new_data["docket_id"] == 67982323, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67982323, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67982323, "decision"] = "affirmed"

# Lets move on to McElrath v. Georgia
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0

new_data.loc[new_data["docket_id"] == 68039948, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 68039948, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 68039948, "decision"] = "reversed and remanded"

# 2022-2023 SCOTUS term data

# Lets start with the case of Arellano v. McDonough
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 66749540, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66749540, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66749540, "decision"] = "affirmed"

# Lets move on to Cruz v. Arizona
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 66833685, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 66833685, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 66833685, "decision"] = "vacated and remanded"

# Lets move on to Bartenwerfer v. Buckley
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 66833686, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66833686, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66833686, "decision"] = "affirmed"

# Lets move on to Helix Energy Solutions Group, Inc. v. Hewitt
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 66833684, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 66833684, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 66833684, "decision"] = "affirmed"

# Lets move on to Bittner v. United States
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66905893, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 66905893, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 66905893, "decision"] = "reversed and remanded"

# Lets move on to Delaware v. Pennsylvania
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be remanded

new_data.loc[new_data["docket_id"] == 66905891, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66905891, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66905891, "decision"] = "remanded"

# Lets move on to Perez v. Sturgis Public Schools
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66738955, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66738955, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66738955, "decision"] = "reversed and remanded"

# Lets move on to Wilkins v. United States
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66576049, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 66576049, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 66576049, "decision"] = "reversed and remanded"

# Lets move on to Axon Enterprise, Inc. v. Federal Trade Commission
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 65737166, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 65737166, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 65737166, "decision"] = "reversed and remanded"

# Lets move on to New York v. New Jersey
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be New Jersey's motion is granted; New York's cross-motion is denied

new_data.loc[new_data["docket_id"] == 67214047, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67214047, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67214047, "decision"] = "New Jersey's motion is granted; New York's cross-motion is denied"

# Lets move on to Reed v. Goertz
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 65414967, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 65414967, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 65414967, "decision"] = "reversed"

# Lets move on to MOAC Mall Holdings LLC v. Transform Holdco LLC
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 66612657, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66612657, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66612657, "decision"] = "vacated and remanded"

# Lets move on to Turkiye Halk Bankasi A.S. v. United States
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be affirmed in part, vacated and remanded in part.

new_data.loc[new_data["docket_id"] == 66735743, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66735743, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66735743, "decision"] = "affirmed in part, vacated and remanded in part."

# Lets move on to National Pork Producers Council v. Ross
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 65414968, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 65414968, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 65414968, "decision"] = "affirmed"

# Lets move on to Percoco v. United States
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66514681, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66514681, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66514681, "decision"] = "reversed and remanded"

# Lets move on to Ciminelli v. United States
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66528499, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66528499, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66528499, "decision"] = "reversed and remanded"

# Lets move on to Financial Oversight and Management Board for Puerto Rico v. Centro de Periodismo Investigativo, Inc.
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66714377, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 66714377, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 66714377, "decision"] = "reversed and remanded"

# Lets move on to Santos-Zacaria v. Garland
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated in part and remanded

new_data.loc[new_data["docket_id"] == 66735159, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66735159, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66735159, "decision"] = "vacated in part and remanded"

# Lets move on to Andy Warhol Foundation for Visual Arts, Inc. v. Goldsmith
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 65419072, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 65419072, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 65419072, "decision"] = "affirmed"

# Lets move on to Ohio Adjutant General's Dept. v. FLRA
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 66708626, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 66708626, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 66708626, "decision"] = "affirmed"

# Lets move on to Twitter, Inc. v. Taamneh
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 66835761, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66835761, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66835761, "decision"] = "reversed"

# Lets move on to Amgen Inc. v. Sanofi
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 67094012, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67094012, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67094012, "decision"] = "affirmed"

# Lets move on to Polselli v. IRS
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 67107270, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67107270, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67107270, "decision"] = "affirmed"

# Lets move on to Arizona v. Mayorkas
# scdb_votes_majority will be None and scdb_votes_minority will be None and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67406125, "scdb_votes_majority"] = None
new_data.loc[new_data["docket_id"] == 67406125, "scdb_votes_minority"] = None
new_data.loc[new_data["docket_id"] == 67406125, "decision"] = "vacated and remanded"

# Lets move on to Sackett v. EPA
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 65396115, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 65396115, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 65396115, "decision"] = "reversed and remanded"

# Lets move on to Dupree v. Younger
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67256513, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67256513, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67256513, "decision"] = "vacated and remanded"

# Lets move on to Tyler v. Hennepin County
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 67272277, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67272277, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67272277, "decision"] = "reversed"

# Lets move on to Glacier Northwest, Inc. v. Teamsters
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66711083, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 66711083, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 66711083, "decision"] = "reversed and remanded"

# Lets move on to Slack Technologies, LLC v. Pirani
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67210302, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67210302, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67210302, "decision"] = "vacated and remanded"

# Lets move on to U.S. ex rel. Schutte v. Supervalu Inc.
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67216342, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67216342, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67216342, "decision"] = "vacated and remanded"

# Lets move on to Health and Hospital Corporation of Marion Cty. v. Talevski
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 65740707, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 65740707, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 65740707, "decision"] = "affirmed"

# Lets move on to Allen v. Milligan
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 65399124, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 65399124, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 65399124, "decision"] = "affirmed"

# Lets move on to Dubin v. United States
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 66894239, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66894239, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66894239, "decision"] = "vacated and remanded"

# Lets move on to Jack Daniel's Properties, Inc. v. VIP Products LLC
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67070569, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67070569, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67070569, "decision"] = "vacated and remanded"

# Lets move on to Haaland v. Brackeen
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be affirmed in part, reversed in part, vacated and remanded in part

new_data.loc[new_data["docket_id"] == 65743884, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 65743884, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 65743884, "decision"] = "affirmed in part, reversed in part, vacated and remanded in part"


# Lets move on to Smith v. United States
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 67102284, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67102284, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67102284, "decision"] = "affirmed"

# Lets move on to Flambeau Band of Lake Superior Chippewa Indians v. Coughlin
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 67257419, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 67257419, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 67257419, "decision"] = "affirmed"

# Lets move on to United States ex rel. Polansky v. Executive Health Resources, Inc.
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 66614594, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 66614594, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 66614594, "decision"] = "affirmed"

# Lets move on to Lora v. United States
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67102775, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67102775, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67102775, "decision"] = "vacated and remanded"

# Lets move on to Jones v. Hendrix
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 65652504, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 65652504, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 65652504, "decision"] = "affirmed"

# Lets move on to Arizona v. Navajo Nation
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 67049554, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 67049554, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 67049554, "decision"] = "reversed"

# Lets move on to Pugin v. Garland
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 67208878, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 67208878, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 67208878, "decision"] = "reversed and remanded"

# Lets move on to Yegiazaryan v. Smagin
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed and remanded

new_data.loc[new_data["docket_id"] == 67264111, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 67264111, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 67264111, "decision"] = "affirmed and remanded"

# Lets move on to United States v. Texas
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 66573480, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 66573480, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 66573480, "decision"] = "reversed"

# Lets move on to Coinbase, Inc. v. Bielski
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 67061316, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 67061316, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 67061316, "decision"] = "reversed and remanded"

# Lets move on to Hansen v. United States
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 67094761, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 67094761, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 67094761, "decision"] = "reversed and remanded"

# Lets move on to Samia v. United States
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 67106124, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 67106124, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 67106124, "decision"] = "affirmed"

# Lets move on to Mallory v. Norfolk Southern R. Co
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 65740073, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 65740073, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 65740073, "decision"] = "vacated and remanded"

# Lets move on to Moore v. Harper
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 66618471, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 66618471, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 66618471, "decision"] = "affirmed"

# Lets move on to Counterman v. Colorado
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67223966, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 67223966, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 67223966, "decision"] = "vacated and remanded"

# Lets move on to Students for Fair Admissions, Inc. v. President and Fellows of Harvard College
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 67538851, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 67538851, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 67538851, "decision"] = "reversed"

# Lets move on to Abitron Austria GmbH v. Hetronic Int'l, Inc.
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67059962, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67059962, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67059962, "decision"] = "vacated and remanded"

# Lets move on to Groff v. DeJoy
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 67215751, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 67215751, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 67215751, "decision"] = "vacated and remanded"

# Lets move onto 303 Creative LLC v. Elenis
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 66612658, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 66612658, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 66612658, "decision"] = "reversed"

# Lets move onto Biden v. Nebraska
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 66908102, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 66908102, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 66908102, "decision"] = "reversed and remanded"

# Lets move onto Department of Education v. Brown
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 66909051, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 66909051, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 66909051, "decision"] = "vacated and remanded"

# 2021-2022 Term

# Lets move onto Department of Homeland Security v. New York
# scbd_votes_majority will be None and scdb_votes_minority will be None and the decision will be dismissed

new_data.loc[new_data["docket_id"] == 16763549, "scdb_votes_majority"] = None
new_data.loc[new_data["docket_id"] == 16763549, "scdb_votes_minority"] = None
new_data.loc[new_data["docket_id"] == 16763549, "decision"] = "dismissed"

# Lets move onto Mississippi v. Tennessee
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be dismissed

new_data.loc[new_data["docket_id"] == 61566933, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 61566933, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 61566933, "decision"] = "dismissed"

# Lets move onto Whole Woman's Health v. Jackson
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be affirmed in part, reversed in part, and remanded

new_data.loc[new_data["docket_id"] == 60333256, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 60333256, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 60333256, "decision"] = "affirmed in part, reversed in part, and remanded"

# Lets move onto United States v. Texas
# scbd_votes_majority will be None and scdb_votes_minority will be None and the decision will be dismissed

new_data.loc[new_data["docket_id"] == 60667676, "scdb_votes_majority"] = None
new_data.loc[new_data["docket_id"] == 60667676, "scdb_votes_minority"] = None
new_data.loc[new_data["docket_id"] == 60667676, "decision"] = "dismissed"

# Lets move onto Babcock v. Kijakazi
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 62546725, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 62546725, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 62546725, "decision"] = "affirmed"

# Lets move onto Hemphill v. New York
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 62610591, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 62610591, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 62610591, "decision"] = "reversed and remanded"

# Lets move onto Hughes v. Northwestern University
# scbd_votes_majority will be 8 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 62622669, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 62622669, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 62622669, "decision"] = "vacated and remanded"

# Lets move onto Unicolors, Inc. v. H&M Hennes & Mauritz, L. P.
# scbd_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 63111509, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63111509, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63111509, "decision"] = "vacated and remanded"

# Lets move onto Cameron v EMW Women's Surgical Center, P. S. C.
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63131039, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63131039, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63131039, "decision"] = "reversed and remanded"

# Lets move onto United States v. Zubaydah
# scbd_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63131038, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 63131038, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 63131038, "decision"] = "reversed and remanded"

# Lets move onto United States v. Tsarnaev
# scbd_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63134643, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63134643, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63134643, "decision"] = "reversed"

# Lets move onto Federal Bureau of Investigation v. Fazaga
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63134644, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63134644, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63134644, "decision"] = "reversed and remanded"

# Lets move onto Wooden v. United States
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63138379, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63138379, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63138379, "decision"] = "reversed and remanded"

# Lets move onto Houston Community College System v. Wilson
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63183500, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63183500, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63183500, "decision"] = "reversed"

# Lets move onto Ramirez v. Collier
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63183499, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63183499, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63183499, "decision"] = "reversed and remanded"

# Lets move onto Badgerow v. Walters
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63202218, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63202218, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63202218, "decision"] = "reversed and remanded"

# Lets move onto Thompson v. Clark
# scbd_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63210618, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63210618, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63210618, "decision"] = "reversed and remanded"

# Lets move onto United States v. Vaello Madero
# scbd_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63252810, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63252810, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63252810, "decision"] = "reversed"

# Lets move onto Brown v. Davenport
# scbd_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63252813, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63252813, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63252813, "decision"] = "reversed"

# Lets move onto City of Austin v. Reagan National Advertising of Austin, LLC
# scbd_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63252811, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63252811, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63252811, "decision"] = "reversed and remanded"

# Lets move onto Boucheler v. Commissioner
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63252814, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63252814, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63252814, "decision"] = "reversed and remanded"

# Lets move onto Cassirer v. Thyssen-Bornemisza Collection Foundation
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 63252812, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63252812, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63252812, "decision"] = "vacated and remanded"

# Lets move onto Cummings v. Premier Rehab Keller
# scbd_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63270152, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63270152, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63270152, "decision"] = "affirmed"

# Lets move onto Shruttleff v. Boston
# scbd_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63279278, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63279278, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63279278, "decision"] = "reversed and remanded"

# Lets move onto Patel v. Garland
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63312348, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63312348, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63312348, "decision"] = "affirmed"

# Lets move onto Federal Election Comm'n v. Ted Cruz
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63312349, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63312349, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63312349, "decision"] = "affirmed"

# Lets move onto Shinn v. Martinez Ramirez
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63329487, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63329487, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63329487, "decision"] = "reversed"

# Lets move onto Morgan v. Sundance, Inc.
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 63329488, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63329488, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63329488, "decision"] = "vacated and remanded"

# Lets move onto Gallardo v. Marstiller
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63393322, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 63393322, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 63393322, "decision"] = "affirmed"


# Lets move onto Southwestern Airlines Co. v. Saxon
# scdb_votes_majority will be 8 and scdb_votes_minority will be 0 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63362546, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63362546, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63362546, "decision"] = "affirmed"

# Lets move onto Siegel v. Fitzgerald
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63362547, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63362547, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63362547, "decision"] = "reversed and remanded"

# Lets move onto Egbert v. Boule
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63369289, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63369289, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63369289, "decision"] = "reversed"

# Lets move onto Johnson v. Arteaga-Martinez
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63379472, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63379472, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63379472, "decision"] = "reversed and remanded"

# Lets move onto Garland v. Gonzalez
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63379473, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63379473, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63379473, "decision"] = "reversed and remanded"

# Lets move onto Denezpi v. United States
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63379474, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63379474, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63379474, "decision"] = "affirmed"

# Lets move onto ZF Automotive U. S., Inc. v. Luxshare, Ltd.
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63379470, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63379470, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63379470, "decision"] = "reversed"

# Lets move onto Kemp v. United States
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63379471, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63379471, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63379471, "decision"] = "affirmed"

# Lets move onto American Hospital Assn. v. Becerra
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63385993, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63385993, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63385993, "decision"] = "reversed and remanded"

# Lets move onto Ysleta del Sur Pueblo v. Texas
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 63385704, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63385704, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63385704, "decision"] = "vacated and remanded"

# Lets move onto Golan v. Saada
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 63385706, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63385706, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63385706, "decision"] = "vacated and remanded"

# Lets move onto Viking River Cruises, Inc. v. Moriana
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63385705, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63385705, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63385705, "decision"] = "reversed and remanded"

# Lets move onto George v. McDonough
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63385991, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63385991, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63385991, "decision"] = "affirmed"


# Lets move onto Carson v. Makin
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63397664, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63397664, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63397664, "decision"] = "reversed and remanded"


# Lets move onto United States v. Taylor
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be affirmed

new_data.loc[new_data["docket_id"] == 63397661, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 63397661, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 63397661, "decision"] = "affirmed"

# Lets move onto Marietta Memorial Hospital Employee Health Benefit Plan v. DaVita, Inc.
# scdb_votes_majority will be 7 and scdb_votes_minority will be 2 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63397663, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 63397663, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 63397663, "decision"] = "reversed and remanded"

# Lets move onto United States v. Washington
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63397660, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63397660, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63397660, "decision"] = "reversed and remanded"

# Lets move onto Shoop v. Twyford
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63397662, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63397662, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63397662, "decision"] = "reversed and remanded"

# Lets move onto Berger v. North Carolina State Conference of the NAACP
# scdb_votes_majority will be 8 and scdb_votes_minority will be 1 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63405003, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 63405003, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 63405003, "decision"] = "reversed"

# Lets move onto Vega v. Tekoh
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63405000, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63405000, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63405000, "decision"] = "reversed and remanded"

# Lets move onto Nance v. Ward
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63405002, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63405002, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63405002, "decision"] = "reversed and remanded"

# Lets move onto Dobbs v. Jackson Women's Health Organization
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63408725, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63408725, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63408725, "decision"] = "reversed and remanded"

# Lets move onto Becerra v. Empire Health Foundation
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63408726, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63408726, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63408726, "decision"] = "reversed and remanded"

# Lets move onto Concepcion v. United States
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63554020, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63554020, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63554020, "decision"] = "reversed and remanded"

# Lets move onto Ruan v. United States (Consolidated with Kahn v. United States)
# scdb_votes_majority will be 9 and scdb_votes_minority will be 0 and the decision will be vacated and remanded

new_data.loc[new_data["docket_id"] == 63549790, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 63549790, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 63549790, "decision"] = "vacated and remanded"

# Lets move onto Kennedy v. Bremerton School District
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed

new_data.loc[new_data["docket_id"] == 63549791, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63549791, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63549791, "decision"] = "reversed"

# Lets move onto Torres v. Texas Department of Public Safety
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63556606, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63556606, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63556606, "decision"] = "reversed and remanded"

# Lets move onto Oklahoma v. Castro-Huerta
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63556607, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63556607, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63556607, "decision"] = "reversed and remanded"

# Lets move onto West Virginia v. Environmental Protection Agency (Consolidated with North American Coal Corporation v. Environmental Protection Agency, Westmoreland Mining Holdings v. Environmental Protection Agency, and North Dakota v. Environmental Protection Agency)
# scdb_votes_majority will be 6 and scdb_votes_minority will be 3 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63560747, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 63560747, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 63560747, "decision"] = "reversed and remanded"

# Lets move onto Biden v. Texas
# scdb_votes_majority will be 5 and scdb_votes_minority will be 4 and the decision will be reversed and remanded

new_data.loc[new_data["docket_id"] == 63560748, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 63560748, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 63560748, "decision"] = "reversed and remanded"

"""
2020-2021 SCOTUS term data
case_name	docket_id	Decision	Vote
Rutledge v. Pharmaceutical Care Management Assn.	18730820	reversed and remanded	8-0
United States v. Briggs	18730818	reversed and remanded	8-0
Carney v. Adams	18730821	vacated and remanded	8-0
Tanzin v. Tanvir	18730819	affirmed	8-0
Texas v. New Mexico	18739724	motion denied	7-1
Chicago v. Fulton	29105324	vacated and remanded	8-0
Salinas v. Railroad Retirement Bd.	59053796	reversed and remanded	5-4
Brownback v. King	59682212	reversed	9-0
United States Fish and Wildlife Serv. v. Sierra Club, Inc.	60045557	reversed and remanded	7-2
Pereida v. Wilkinson	59703959	affirmed	5-3
Uzuegbunam v. Preczewski	59711939	reversed and remanded	8-1
Ford Motor Co. v. Montana Eighth Judicial Dist.	59763138	affirmed	8-0
FCC v. Prometheus Radio Project	59780908	reversed	9-0
Facebook, Inc. v. Duguid	59780907	reversed and remanded	9-0
Google LLC v. Oracle America, Inc.	59796974	reversed and remanded	6-2
Jones v. Mississippi	59844618	affirmed	6-3
Carr v. Saul	59844620	reversed and remanded	9-0
AMG Capital Management, LLC v. FTC	59844621	reversed and remanded	9-0
Niz-Chavez v. Garland	59864544	reversed	6-3
Edwards v. Vannoy	59911203	affirmed	6-3
BP p.l.c. v. Mayor and City Council of Baltimore	59911206	vacated and remanded	7-1
CIC Servs., LLC v. IRS	59911205	reversed and remanded	9-0
Caniglia v. Strom	59911204	vacated and remanded	9-0
United States v. Palomar-Santiago	59929479	reversed and remanded	9-0
Guam v. United States	59929480	reversed and remanded	9-0
San Antonio v. Hotels.com, L. P.	59940352	affirmed	9-0
Garland v. Ming Dai	59951434	vacated and remanded	9-0
United States v. Cooley	59951433	vacated and remanded	9-0
Sanchez v. Mayorkas	59964669	affirmed	9-0
Borden v. United States	59974422	reversed and remanded	5-4
Greer v. United States	59982316	affirmed	9-0
Terry v. United States	59982315	affirmed	9-0
California v. Texas	59992709	reversed and remanded	7-2
Nestlé USA, Inc. v. Doe	59992707	reversed and remanded	8-1
Fulton v. Philadelphia	59992708	reversed and remanded	9-0
United States v. Arthrex, Inc.	59999711	vacated and remanded	5-4
Goldman Sachs Group, Inc. v. Arkansas Teacher Retirement System	59999713	vacated and remanded	8-1
National Coalition for Men v. Selective Service System	60000772	affirmed	9-0
Lange v. California	60006480	vacated and remanded	9-0
Collins v. Yellen	60008371	affirmed in part, reversed in part, vacated in part, and remanded	7-2
Mahanoy Area School Dist. v. B. L.	60006479	affirmed	8-1
Cedar Point Nursery v. Hassid	60006482	reversed and remanded	6-3
TransUnion LLC v. Ramirez	60013646	reversed and remanded	5-4
HollyFrontier Cheyenne Refining, LLC v. Renewable Fuels Assn.	60013650	reversed	6-3
Yellen v. Confederated Tribes of Chehalis Reservation	60089120	reversed and remanded	6-3
Lombardo v. St. Louis	67543949	vacated and remanded	6-3
Minerva Surgical, Inc. v. Hologic, Inc.	60021624	vacated and remanded	5-4
Johnson v. Guzman Chavez	60021625	reversed	6-3
PennEast Pipeline Co. v. New Jersey	60021623	reversed and remanded	5-4
Brnovich v. Democratic National Committee	60030940	reversed and remanded	6-3
Americans for Prosperity Foundation v. Bonta	60030942	reversed and remanded	6-3
"""

new_data.loc[new_data["docket_id"] == 18730820, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 18730820, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 18730820, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 18730818, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 18730818, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 18730818, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 18730821, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 18730821, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 18730821, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 18730819, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 18730819, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 18730819, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 18739724, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 18739724, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 18739724, "decision"] = "motion denied"

new_data.loc[new_data["docket_id"] == 29105324, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 29105324, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 29105324, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 59053796, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 59053796, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 59053796, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59682212, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59682212, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59682212, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 60045557, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 60045557, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 60045557, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59703959, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 59703959, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 59703959, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59711939, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 59711939, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 59711939, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59763138, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 59763138, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59763138, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59780908, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59780908, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59780908, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 59780907, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59780907, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59780907, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59796974, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 59796974, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 59796974, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59844618, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 59844618, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 59844618, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59844620, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59844620, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59844620, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59844621, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59844621, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59844621, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59864544, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 59864544, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 59864544, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 59911203, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 59911203, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 59911203, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59911206, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 59911206, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 59911206, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 59911205, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59911205, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59911205, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59911204, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59911204, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59911204, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 59929479, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59929479, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59929479, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59929480, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59929480, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59929480, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59940352, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59940352, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59940352, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59951434, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59951434, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59951434, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 59951433, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59951433, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59951433, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 59964669, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59964669, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59964669, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59974422, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 59974422, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 59974422, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59982316, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59982316, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59982316, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59982315, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59982315, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59982315, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59992709, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 59992709, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 59992709, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59992707, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 59992707, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 59992707, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59992708, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 59992708, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 59992708, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 59999711, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 59999711, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 59999711, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 59999713, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 59999713, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 59999713, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 60000772, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 60000772, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 60000772, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 60006480, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 60006480, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 60006480, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 60008371, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 60008371, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 60008371, "decision"] = "affirmed in part, reversed in part, vacated in part, and remanded"

new_data.loc[new_data["docket_id"] == 60006479, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 60006479, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 60006479, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 60006482, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 60006482, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 60006482, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 60013646, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 60013646, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 60013646, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 60013650, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 60013650, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 60013650, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 60089120, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 60089120, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 60089120, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 67543949, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 67543949, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 67543949, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 60021624, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 60021624, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 60021624, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 60021625, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 60021625, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 60021625, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 60021623, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 60021623, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 60021623, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 60030940, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 60030940, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 60030940, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 60030942, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 60030942, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 60030942, "decision"] = "reversed and remanded"

# 2019-2020 SCOTUS term data
"""
Rotkiske v. Klemm,affirmed,8-1,16566496
Peter v. NantKwest, Inc.,affirmed,9-0,16571806
Ritzen Group, Inc. v. Jackson Masonry, LLC,affirmed,9-0,16689796
McKinney v. Arizona,affirmed,5-4,59844618
Rodriguez v. Federal Deposit Insurance Corporation,vacated and remanded,9-0,16885818
Hernandez v. Mesa,affirmed,5-4,15782883
Monasky v. Taglieri,affirmed,9-0,16885819
Intel Corp. Investment Policy Committee v. Sulyma,affirmed,9-0,16891172
Holguin-Hernandez v. United States,vacated and remanded,9-0,16891173
Shular v. United States,affirmed,9-0,16891171
Kansas v. Garcia,reversed and remanded,5-4,16919687
Comcast Corp. v. National Association of African American-Owned Media,vacated and remanded,9-0,17001687
Allen v. Cooper,affirmed,9-0,17001688
Kahler v. Kansas,affirmed,6-3,17001684
Guerrero-Lasprilla v. Barr,vacated and remanded,7-2,17001685
CITGO Asphalt Refining Co. v. Frescati Shipping Co., Ltd.,affirmed,7-2,17022742
Kansas v. Glover,reversed and remanded,8-1,17045004
Babb v. Wilkie,reversed and remanded,8-1,17045005
Ramos v. Louisiana,reversed,6-3,17081725
Atlantic Richfield Co. v. Christian,"affirmed in part, vacated in part, and remanded",7-2,17081726
Thryv, Inc. v. Click-To-Call Technologies, LP,vacated and remanded,7-2,17081724
Barton v. Barr,affirmed,5-4,17093261
County of Maui, Hawaii v. Hawaii Wildlife Fund,vacated and remanded,6-3,17093260
Romag Fasteners, Inc. v. Fossil, Inc.,vacated and remanded,9-0,17093259
Maine Community Health Options v. United States,reversed and remanded,8-1,17102120
Georgia v. Public.Resource.Org, Inc.,affirmed,5-4,17102122
Kelly v. United States,reversed and remanded,9-0,17136831
United States v. Sineneng-Smith,vacated and remanded,9-0,17136830
Lucky Brand Dungarees, Inc. v. Marcel Fashions Group, Inc.,reversed and remanded,9-0,17163210
Opati v. Republic of Sudan,vacated and remanded,8-0,17171263
Financial Oversight and Management Bd. for Puerto Rico v. Aurelius Investment, LLC,reversed and remanded,9-0,17211560
Nasrallah v. Barr,reversed,7-2,17211558
Banister v. Davis,reversed and remanded,7-2,17211561
Thole v. U.S. Bank,affirmed,5-4,17211557
GE Energy Power Conversion France SAS, Corp. v. Outokumpu Stainless USA, LLC,reversed and remanded,9-0,17211559
Lomax v. Ortiz-Marquez,affirmed,9-0,17230039
United States Forest Service v. Cowpasture River Preservation Association,reversed and remanded,7-2,17248923
Bostock v. Clayton County,reversed and remanded,6-3,17248924
Department of Homeland Security v. Regents of the University of California,vacated in part and reversed in part,5-4,17259766
Liu v. Securities and Exchange Commission,vacated and remanded,8-1,17280841
Department of Homeland Security v. Thuraissigiam,reversed and remanded,7-2,17292962
USAID v. Alliance for Open Society International,reversed,5-3,17302334
June Medical Services LLC v. Russo,reversed,5-4,17302333
Seila Law LLC v. Consumer Financial Protection Bureau,vacated and remanded,5-4,17302332
Espinoza v. Montana Department of Revenue,reversed and remanded,5-4,17307166
United States Patent and Trademark Office v. Booking.com B.V.,affirmed,8-1,17307165
Barr v. American Association of Political Consultants Inc.,affirmed,6-3,17323190
Chiafalo v. Washington,affirmed,9-0,17323189
Little Sisters of the Poor Saints Peter and Paul Home v. Pennsylvania,reversed and remanded,7-2,17330513
Our Lady of Guadalupe School v. Morrissey-Berru,reversed and remanded,7-2,17330512
McGirt v. Oklahoma,reversed,5-4,17334317
Trump v. Vance,affirmed and remanded,7-2,17334314
Trump v. Mazars USA,vacated and remanded,7-2,17334315
"""

new_data.loc[new_data["docket_id"] == 16566496, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 16566496, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 16566496, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16571806, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16571806, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16571806, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16689796, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16689796, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16689796, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 59844618, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 59844618, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 59844618, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16885818, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16885818, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16885818, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 15782883, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 15782883, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 15782883, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16885819, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16885819, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16885819, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16891172, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16891172, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16891172, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16891173, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16891173, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16891173, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 16891171, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 16891171, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 16891171, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 16919687, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 16919687, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 16919687, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17001687, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17001687, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17001687, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17001688, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17001688, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17001688, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17001684, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 17001684, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 17001684, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17001685, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17001685, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17001685, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17022742, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17022742, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17022742, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17045004, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 17045004, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 17045004, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17045005, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 17045005, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 17045005, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17081725, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 17081725, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 17081725, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 17081726, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17081726, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17081726, "decision"] = "affirmed in part, vacated in part, and remanded"

new_data.loc[new_data["docket_id"] == 17081724, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17081724, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17081724, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17093261, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17093261, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17093261, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17093260, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 17093260, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 17093260, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17093259, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17093259, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17093259, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17102120, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 17102120, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 17102120, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17102122, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17102122, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17102122, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17136831, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17136831, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17136831, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17136830, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17136830, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17136830, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17163210, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17163210, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17163210, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17171263, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 17171263, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17171263, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17211560, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17211560, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17211560, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17211558, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17211558, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17211558, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 17211561, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17211561, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17211561, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17211557, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17211557, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17211557, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17211559, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17211559, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17211559, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17230039, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17230039, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17230039, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17248923, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17248923, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17248923, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17248924, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 17248924, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 17248924, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17259766, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17259766, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17259766, "decision"] = "vacated in part and reversed in part"

new_data.loc[new_data["docket_id"] == 17280841, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 17280841, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 17280841, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17292962, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17292962, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17292962, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17302334, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17302334, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 17302334, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 17302333, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17302333, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17302333, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 17302332, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17302332, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17302332, "decision"] = "vacated and remanded"

new_data.loc[new_data["docket_id"] == 17307166, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17307166, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17307166, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17307165, "scdb_votes_majority"] = 8
new_data.loc[new_data["docket_id"] == 17307165, "scdb_votes_minority"] = 1
new_data.loc[new_data["docket_id"] == 17307165, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17323190, "scdb_votes_majority"] = 6
new_data.loc[new_data["docket_id"] == 17323190, "scdb_votes_minority"] = 3
new_data.loc[new_data["docket_id"] == 17323190, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17323189, "scdb_votes_majority"] = 9
new_data.loc[new_data["docket_id"] == 17323189, "scdb_votes_minority"] = 0
new_data.loc[new_data["docket_id"] == 17323189, "decision"] = "affirmed"

new_data.loc[new_data["docket_id"] == 17330513, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17330513, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17330513, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17330512, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17330512, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17330512, "decision"] = "reversed and remanded"

new_data.loc[new_data["docket_id"] == 17334317, "scdb_votes_majority"] = 5
new_data.loc[new_data["docket_id"] == 17334317, "scdb_votes_minority"] = 4
new_data.loc[new_data["docket_id"] == 17334317, "decision"] = "reversed"

new_data.loc[new_data["docket_id"] == 17334314, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17334314, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17334314, "decision"] = "affirmed and remanded"

new_data.loc[new_data["docket_id"] == 17334315, "scdb_votes_majority"] = 7
new_data.loc[new_data["docket_id"] == 17334315, "scdb_votes_minority"] = 2
new_data.loc[new_data["docket_id"] == 17334315, "decision"] = "vacated and remanded"

# Had to add that one column values for 2018-2019 term

new_data.loc[new_data["docket_id"] == 8497101, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 8497102, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 8502087, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 8502088, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14560167, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 14560168, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14570112, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14572838, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14581867, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 14572837, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14581864, "decision"] = "reversed in part and remanded"
new_data.loc[new_data["docket_id"] == 14581865, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14589881, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14741675, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14741676, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14741674, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14752731, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14797494, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14797493, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 14808987, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14846760, "decision"] = "affirmed" 
new_data.loc[new_data["docket_id"] == 14846761, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 14988889, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15013727, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15421413, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15421414, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15421415, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15645451, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15645452, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15682000, "decision"] = "reversed and remanded"  
new_data.loc[new_data["docket_id"] == 15682002, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15682001, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15719361, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15714963, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15714962, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15714960, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15740684, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15740685, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15740686, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15785703, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15782885, "decision"] = "reversed in part and remanded"
new_data.loc[new_data["docket_id"] == 15782883, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15782884, "decision"] = "appeal dismissed"
new_data.loc[new_data["docket_id"] == 15808705, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15808758, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15808734, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15808684, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15816342, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15816344, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15816343, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15823030, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15823029, "decision"] = "reversed and remanded" 
new_data.loc[new_data["docket_id"] == 15823025, "decision"] = "affirmed in part, vacated in part, and remanded"
new_data.loc[new_data["docket_id"] == 15823028, "decision"] = "reversed and remanded"
new_data.loc[new_data["docket_id"] == 15823027, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15835815, "decision"] = "affirmed"
new_data.loc[new_data["docket_id"] == 15835814, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15835816, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15843615, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15843614, "decision"] = "vacated and remanded"
new_data.loc[new_data["docket_id"] == 15843616, "decision"] = "affirmed in part, reversed in part, and remanded"

# Check for duplicates in the 'case_name' column
duplicates = new_data[new_data.duplicated(subset='case_name', keep=False)]

# Filter out duplicates where all rows have NaN in 'scdb_votes_majority'
filtered_duplicates = duplicates.groupby('case_name').filter(lambda x: x['scdb_votes_majority'].notna().any())

final_data = pd.concat([new_data.drop_duplicates(subset='case_name', keep=False), filtered_duplicates])

single_row_cases = final_data.groupby('case_name').filter(lambda x: len(x) == 1)
cases_to_drop = single_row_cases[single_row_cases['scdb_votes_majority'].isna()]['case_name'].unique()
final_data = final_data[~final_data['case_name'].isin(cases_to_drop)]

# send this to a excel file
final_data.to_excel("C:\\Users\\Kory\\Downloads\\full_data.xlsx")



# store the new data as a pickle

final_data.to_pickle("C:\\Users\\Kory\\Downloads\\full_data.pickle")


