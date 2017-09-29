###A. Some things:###

1) You must install the pure python library "websocket-client" (https://pypi.python.org/pypi/websocket-client) with "pip install websocket-client". Use StaSh library for Pythonista.

2) "sage_interface.py" uses the server "https://sagecell.sagemath.org/" to perform calculations.

3) The scripts works in your Python personal environment (not only Pythonista), but:
	-) the scripts are for Python2;
	-) to be sure to obtain a valid answer from the server you should add a 'time.sleep(1)' before any 'print(var)' in the 'input_sage_XX.py' scripts. I don't know why but in this way it works well.
	-) in 'input_sage_XX.py' scripts you should add 'print(var)' if you want to print and save the variable 'var' to use it in Pythonista environment. If you execute a 'input_sage_XX.py' without any 'print(...)' inside, 'sage_interface.py' can't process the output string returned by the server.
	-) ...










###B. Some improvements about scripts version 29-09-2017 compared to version 15-09-2017:###

1) Now the main script 'sage_test.py' runs until the server returns a solution (the timeout is increased automatically if the server is busy and the main script is executed X times until server math full output).

2) Now you can pass some Pythonista variables to the server (see 'sage_test.py' main script and the function 'execute_sage_script_w_inputs').

3) For now, you must manually evaluate/process the output from server that is a list of strings: you need to evaluate what you want, convert the string into a valid Python object (for numpy, as example) and use it. Only numbers are correctly evaluated.

4) ...








###C. Possible future improvements:###

1) return arrays, images, videos, plots, any external files available for Pythonista.

2) convert some useful opensource not-pure libraries in order to use them with SageMathCell (in order to be able to use Pythonista console to run full scipy commands in the common way: >>> from scipy.interpolate import interp1d ...).

3) ... 









Please improve what you want if you want about these scripts. If your solution seems better, I'd like to learn your solution. Use Pythonista forum.


Many Thanks to:
-) "websocket-client" authors;
-) SageMathCell servers maintainers and authors;
-) stackoverflow (for very skilled solutions);
-) Pythonista users: JonB for wrench version of 'sage_interface.py' (you can use it to find syntax errors in the script passed to server SageMathCell) and ccc for suggestions about JSON (I'm still learning it...);
-) obviously Omz for his Pythonista (Full IDE that works in a small/smart device like iPhone)!