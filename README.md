# Snowball #
*A lightweight, cross-platform data mining utility*

Snowball makes it easy to quickly get information about hardware usage 
statistics and process information.

----------

### Using Snowball ###

> **Note:** Code examples are written for Ubuntu Linux and may not work with 
other operating systems

Before beginning, make sure all dependencies are met, or Snowball will not run. 
See the *Dependency Information* section for more information. To run Snowball, 
simply run

    ./snowball.py

in Snowball's directory, and Snowball will write its output to the console. 
Information is collected in the order of volatility, which means that the 
information most likely to change is collected first, and more constant 
information is collected last. It's also possible to write Snowball's output to 
a log file:

    ./snowball.py > log-name.txt
    
All of the information collected by Snowball will be sent into the log file for 
easy access later.

----------

### Dependency Information ###

Snowball has some requirements before it will run. First off, make sure you 
have [Python 3.3][1] or newer. Then, install [psutil][2] 1.2.1. It's recommended 
that you install psutil using [pip][3] to ensure that psutil will be installed 
correctly.

**Ubuntu:**
To install Python 3.3, run

    sudo apt-get install python3

To install pip, run

    sudo apt-get install python3-pip

After pip is installed, run

    sudo pip3 install psutil
    
**Windows:**

To install Python 3.3, download and install it from the link above. Then, 
download and run [pip-Win][4]. Follow the instructions on the page provided.

> **Note:** psutil requires a C compiler to install properly. Install [Visual 
C++ 2010 Express][5]; if you're on a 64-bit system, follow the instructions in 
[this article][6]. If you don't want to do this, you can install an 
[unsupported 
precompiled binary][7], but this is not recommended.

----------

### Notes ###

Snowball is still in its initial alpha stage of testing and release, so many 
features may not work and there may be bugs present in the code. Snowball may 
also change drastically from commit to commit.

  [1]: http://www.python.org/download/releases/3.3.3/
  [2]: http://code.google.com/p/psutil/
  [3]: https://pypi.python.org/pypi/pip
  [4]: https://sites.google.com/site/pydatalog/python/pip-for-windows
  [5]: http://www.visualstudio.com/en-us/downloads/download-visual-studio-vs#DownloadFamilies_4
  [6]: http://kb-en.radiantzemax.com/KnowledgebaseArticle50286.aspx
  [7]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#psutil
