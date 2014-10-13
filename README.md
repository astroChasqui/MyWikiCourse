#MyWikiCourse

This is my first Flask project. The idea is to be able to use Wikipedia as your class textbook for your subject of interest. The app organizes the content and remains wikipedia-updated.

##virtualenv

I struggled a bit to make virtualenv work for this project given my preferences. I use both Linux and Windows machines, so a unique solution was hard to find. I ended up using a combination of conda and pip.

~~~
conda create --name mwc --file requirements_conda.txt
activate mwc
pip install -r requirements_pip.txt
~~~

The need for pip stems from my failure to make conda install Flask extensions. With pip on Windows, on the other hand, I have not been able to install ipython notebook in a virtualenv, so this is my preferred method for now. Actually I don't use the notebook for this project, but since this happened in other projects, I carry it here as well. It is possible that this project could be installed with pip alone. The requirements_pip.txt file includes packages that can also be installed with conda, but since it is used later, they are ignored.
