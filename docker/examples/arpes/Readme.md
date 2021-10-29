pyARPES in webtop guacamole
===========================

This a draft implementation substantiating how pyARPES can be executed in a webtop linux guacamole server.
The following procedure worked for me.
In a local directory on my computer (Ubuntu) I placed:
Dockerfile		The build recipe
Test.ipynb 		Tommaso example Jupyter notebook with Qt test visualizations and links to example data
FireUpPyArpes.bash  	script which solves, maybe not in the most elegant way, activation of conda in guacd

* docker build -t arpes-webtop-test .
* docker run -p 5000:3000 arpes-webtop-test
* Surf to localhost:5000 in your browser
* A console in the browser will be displayed where you are user abc (non-root, interestingly) use echo $UID and whoami to confirm
* source FireUpPyArpes.bash, this will activate conda in the running container and take ownership of only the
/pyarpes/v3/python-arpes/research directory and sub-directories in there

Ideally a jupyter-notebook should come up with a single Test.ipynb that you can then click through
and enjoy Tommaso nice arpes Qt visualization

Once your done you can close the browser, but that will not close the container for this
* docker ps
* and then inspect the first column value CONTAINER ID
* docker stop <CONTAINER ID> to stop the service completely
