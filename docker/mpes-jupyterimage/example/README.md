# Introduction

This example presents the capabilities of the NOMAD platform to store and standardize multi photoemission spectroscopy (MPES) experimental data. It contains three major examples:

- Taking a pre-binned file, here stored in a h5 file, and converting it into the standardized MPES NeXus format. There exists a [NeXus application definition for MPES](https://manual.nexusformat.org/classes/contributed_definitions/NXmpes.html#nxmpes) which details the internal structure of such a file.
- Binning of raw data (see [here](https://www.nature.com/articles/s41597-020-00769-8) for additional resources) into a h5 file and consecutively generating a NeXus file from it.
- An analysis example taking data in the NeXus format and employing the [pyARPES](https://github.com/chstan/arpes) analysis tool to reproduce the main findings of [this paper](https://arxiv.org/pdf/2107.07158.pdf).

# Viewing uploaded data

Here you find an overview of your uploaded data.
Click on the `> /` button to get a list of your data or select **FILES** from the top menu of this upload.
You may add your own files to the upload or experiment with the pre-existing electronic lab book example.
The ELN follows the general structure of NOMAD ELN templates and you may refer to the [official documentation](link me)
on how to work with it.
When the ELN is saved a NeXus file will be generated from the provided example data.
You may also view your supplied or generated NeXus files here with the H5Web viewer.
To do so open the **FILES** tab and just select a `.nxs` file.

# Analysing the data

This example works through the use of the NOMAD remote tools hub (NORTH) containers, i.e. besides using and dealing with the uploaded MPES data a container can be started to analyise the data. If you want to execute the examples locally, please refer to the `INSTALL.md` file in this directory.
In the container you're presented three example notebooks containing the aformentioned examples.

To start an analysis, note your upload id (which you find on top of this explanation) and select **ANALYZE** from the top menu, then **NOMAD Remote Tools Hub**.
In the appearing list you'll find the ARPES Example, click on it and click **LAUNCH**.
After a few moments a new tab will open which displays a jupyter environment providing the required analysis tools.
To find the examples navigate to uploads inside the jupyter hub browser and select the folder with your noted upload id.
There you'll find the example `ipynb` notebooks.
Double-clicking each of the notebooks will open the examples in the jupyter main window.
From here you find detailed instructions inside the notebooks.

# Where to go from here?

If your interested in using this pipeline for your experiment you find support at FAIRmat or ... etc.
If you have questions regarding the experiments in the examples you may contact ... from the working group of Laurenz Rettig at the Fritz-Haber Institute Berlin, who provided the examples.
For general questions regarding the ARPES pipeline and if you're interested in building one for your
own research workflow you may contact [Florian Dobener](mailto:florian.dobener@physik.hu-berlin.de) from the FAIRmat consortium.
