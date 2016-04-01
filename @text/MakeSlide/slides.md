% Title
% Name
% Date


My first slide
--------------------

List

* this 
* is
* cool

Variables
---------

The following variables can be defined from the command line:

* theme
* transition

```bash
pandoc -t html5 --template=revealjs.html \
	--standalone --section-divs \
  --variable theme="beige" \
  --variable transition="linear" \
  slides.md -o slides.html
```

```python
python makeslide.py slides -r slide -t beige
```
