library(reticulate)
install_miniconda()
#miniconda_update()
reticulate::use_condaenv("base")

# Install the datasets library if it's not already installed
py_run_string("import os; os.system('pip install datasets')")

# Import the datasets library from Python
datasets <- import("datasets")


pile_of_law <- datasets$load_dataset("pile-of-law/pile-of-law", "courtlistener_opinions")
pile_of_law_train<- py_to_r(pile_of_law$train)
pile_of_law_test<- py_to_r(pile_of_law$validation)

pile_of_law_df<-rbind(pile_of_law_train,pile_of_law_test)
