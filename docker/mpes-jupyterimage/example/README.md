# Introduction
This example presents the capabilities of the NOMAD platform to store and standardize multi photoemission spectroscopy (MPES) experimental data. It contains three major examples:
- Taking a binned file, here stored in a h5 file, and converting it into the standardized MPES NeXus format. There exists a NeXus application definition for MPES which details the internal structure of such a file (ToDo: Link to the newest version at FAIRmat proposal).
- Binning of raw data (see [here](https://www.nature.com/articles/s41597-020-00769-8) for additional resources) into an h5 file and consecutively generating a NeXus file from it.
- An analysis example to work with NeXus files and make use of its stored metadata. (ToDo: What is this example?)

# Viewing uploaded data
Below you find an overview of your uploaded data.
-> Explain what can be done with the data at this stage?
-> Can we view it somehow?
-> ELN functionality
-> Conjuction with ELN and measurement data

# Analysing the data
This example works through the use of the NOMAD remote tools hub (NORTH) containers, i.e. besides using and dealing with the uploaded MPES data a container can be started to analyise the data. If you want to execute the examples locally, please refer to the `INSTALL.md` file in this directory.
In the container you're presented three example notebooks containing the aformentioned examples.

-> Can we create a link to start the container?
-> Otherwise explain how to navigate to the container and how to start it
-> Give a short explanation on what will be visible on the server
-> Write a kickoff README for in the Jupyter Notebooks

# Where to go from here?
If your interested in using this pipeline for your experiment you find support at FAIRmat or ... etc. 
-> Do we want to include something like this?
-> Local install routines. Link an INSTALL.md which explains the setup on a local computer (with or w/o docker)