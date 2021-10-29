#!/bin/bash

cd /pyarpes/v3/python-arpes/
export PATH=/pyarpes/v3/thirdparty/miniconda/bin:$PATH
conda init bash
source ~/.bashrc
cd /pyarpes/v3/python-arpes/
conda activate arpes
sudo chown -cR abc research
cd research
chmod +x Test.ipynb
jupyter-notebook

