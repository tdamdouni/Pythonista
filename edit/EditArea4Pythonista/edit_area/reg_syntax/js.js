// patch applied: https://sourceforge.net/tracker/?func=detail&aid=3107951&group_id=164008&atid=829999

// resorted and then augmented

editAreaLoader.load_syntax["js"] = {
	'DISPLAY_NAME' : 'Javascript'
	,'COMMENT_SINGLE' : {1 : '//'}
	,'COMMENT_MULTI' : {'/*' : '*/'}
	,'QUOTEMARKS' : {1: "'", 2: '"'}
	,'KEYWORD_CASE_SENSITIVE' : false
	,'KEYWORDS' : {
		'statements' : [
			'as',
			'break',
			'case',
			'catch',
			'continue',
			'decodeURI',
			'delete',
			'do',

			'else',
			'encodeURI',
			'eval',
			'finally',
			'for',
			'if',
			'in',
			'is',
			'item',

			'instanceof',
			'return',
			'switch',
			'this',
			'throw',
			'try',
			'typeof',
			'void',

			'while',
			'write',
			'with'
		]
		,'keywords' : [
			'abstract',
			'Anchor',
			'Area',
			'Array',
			'assign',
			'Boolean',
			'Button',
			'byte',
			'callee',
			'char',
			'Checkbox',
			'class',
			'closed',
			'const',
			'constructor',
			'Date',
			'debugger',
			'default',
			'defaultStatus',
			'document',
			'double',
			'Element',
			'export',
			'extends',
			'false',
			'FileUpload',
			'final',
			'float',
			'Form',
			'Frame',
			'frames',
			'function',
			'getClass',
			'goto',
			'Hidden',
			'History',
			'Image',
			'implements',
			'import',
			'Infinity',
			'innerHeight',
			'innerWidth',
			'java',
			'JavaArray',
			'JavaClass',
			'JavaObject',
			'JavaPackage',
			'length',
			'Link',
			'location',
			'locationbar',
			'long',
			'Math',
			'menubar',
			'MimeType',
			'namespace',
			'NaN',
			'native',
			'navigator',
			'netscape',
			'new',
			'null',
			'Number',
			'Object',
			'onBlur',
			'onError',
			'onFocus',
			'onLoad',
			'onUnload',
			'opener',
			'Option',
			'outerHeight',
			'outerWidth',
			'package',
			'Packages',
			'pageXoffset',
			'pageYoffset',
			'parent',
			'Password',
			'personalbar',
			'Plugin',
			'private',
			'protected',
			'prototype',
			'public',
			'Radio',
			'ref',
			'RegExp',
			'Reset',
			'scrollbars',
			'Select',
			'self',
			'short',
			'statusbar',
			'String',
			'Submit',
			'sun',
			'super',
			'synchronized',
			'Text',
			'Textarea',
			'throws',
			'toolbar',
			'top',
			'transient',
			'true',
			'use',
			'var',
			'window'
		]
		,'functions' : [
			// common functions for Window object
			'alert',
			'arguments',
			'back',
			'blur',
			'caller',
			'captureEvents',
			'clearInterval',
			'clearTimeout',
			'close',
			'confirm',
			'escape',
			'eval',
			'find',
			'focus',
			'forward',
			'handleEvent',
			'home',
			'isFinite',
			'isNan',
			'moveBy',
			'moveTo',
			'name',
			'navigate',
			'onblur',
			'onerror',
			'onfocus',
			'onload',
			'onmove',
			'onresize',
			'onunload',
			'open',
			'parseFloat',
			'parseInt',
			'print',
			'prompt',
			'releaseEvents',
			'resizeBy',
			'resizeTo',
			'routeEvent',
			'scroll',
			'scrollBy',
			'scrollTo',
			'setInterval',
			'setTimeout',
			'status',
			'stop',
			'taint',
			'toString',
			'unescape',
			'untaint',
			'unwatch',
			'valueOf',
			'watch'
		]
	}
	,'OPERATORS' :[
		'+', '-', '/', '*', '=', '<', '>', '%', '!'
	]
	,'DELIMITERS' :[
		'(', ')', '[', ']', '{', '}'
	]
	,'STYLES' : {
		'COMMENTS': 'color: #AAAAAA;'
		,'QUOTESMARKS': 'color: #6381F8;'
		,'KEYWORDS' : {
			'statements' : 'color: #60CA00;'
			,'keywords' : 'color: #48BDDF;'
			,'functions' : 'color: #2B60FF;'
		}
		,'OPERATORS' : 'color: #FF00FF;'
		,'DELIMITERS' : 'color: #0038E1;'

	}
	,'AUTO_COMPLETION' :  {
		"default": {    // the name of this definition group. It's posisble to have different rules inside the same definition file
			"REGEXP": { "before_word": "[^a-zA-Z0-9_]|^"    // \\s|\\.|
						,"possible_words_letters": "[a-zA-Z0-9_]+"
						,"letter_after_word_must_match": "[^a-zA-Z0-9_]|$"
						,"prefix_separator": "\\."
					}
			,"CASE_SENSITIVE": true
			,"MAX_TEXT_LENGTH": 100     // the maximum length of the text being analyzed before the cursor position
			,"KEYWORDS": {
				'': [   // the prefix of thoses items
						/**
						 * 0 : the keyword the user is typing
						 * 1 : (optionnal) the string inserted in code ("{@}" being the new position of the cursor, "§" beeing the equivalent to the value the typed string indicated if the previous )
						 *      If empty the keyword will be displayed
						 * 2 : (optionnal) the text that appear in the suggestion box (if empty, the string to insert will be displayed)
						 */
						 ['Array', '§()', '']
						,['alert', '§({@})', 'alert(String message)']
						,['document']
						,['window']
					]
				,'window' : [
						 ['location']
						,['document']
						,['scrollTo', 'scrollTo({@})', 'scrollTo(Int x,Int y)']
					]
				,'location' : [
						 ['href']
					]
			}
		}
	}
};
