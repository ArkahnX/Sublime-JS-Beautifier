Installing
----------
1) First, install **[JS Beautifier](https://github.com/einars/js-beautify)**

	git clone https://github.com/einars/js-beautify

	cd js-beautify/python

	sudo python ./setup.py install

Notice: Sublime is using python 2.6 defaultly. If your python version is not 2.6 then use

	sudo python-2.6 ./setup.py install

2) Then install this Sublime plugin

**With the [Package Control plugin](http://wbond.net/sublime_packages/package_control):** 
Add [my package channel](
https://github.com/cancerhermit/Sublime-package-channel)
url - 

	https://raw.github.com/cancerhermit/Sublime-package-channel/master/repositories.json

Bring up the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows). Select "Package Control: Install Package", wait while Package Control fetches the latest package list, then select **JS Beautifier** when the list appears. The advantage of using this method is that Package Control will automatically keep plugins up to date with the latest version.

**Without Git:** Download the latest source from [GitHub](https://github.com/cancerhermit/Sublime-js-beautifier) and copy the Sublime-js-beautifier folder to your Sublime Text "Packages" directory.

**With Git:** Clone the repository in your Sublime Text "Packages" directory:

    git clone https://github.com/cancerhermit/Sublime-js-beautifier.git


The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

        ~/.config/sublime-text-2/Packages/

* Windows:

        %APPDATA%/Sublime Text 2/Packages/

Usage
----------
Just save. Plugin use **on_pre_save** EventListener