From start to finish, I will give my instructions on what I did for reproducibility standards:

Do not forget to change the API Keys and the location of where your pickle and feathers files are being held and saved. 

1. Create your account https://www.courtlistener.com/register/?next=/help/api/rest/ here, and then you will be able to get your API key.
2. Run download_clusters.ipynb
3. I ran clusters_to_opinions_originals.ipynb (but then it stopped running in the middle of it, so I had to think of a workaround)
4. I ran clusters_to_opinions_fix.ipynb to get the rest of the opinions
5. I ran opinions_to_authors.ipynb to get the authors
6. I ran clusters_to_dockets_id.ipynb to get the dockets.
7. I ran data cleaning amd merging.ipynb to get the data in a clean enough state.
8. I ran preFeatherDataCleaning.ipynb to get the full data pickle file.
9. I ran PuttingFileIntoDatabase.ipynb where I could get the Data from R
   because when I tried to put the feather file into R directly, it became too laggy to work with. 


Note: it was a very arduous task
