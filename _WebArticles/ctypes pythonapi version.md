# ctypes pythonapi version

_Captured: 2016-07-01 at 01:43 from [forum.omz-software.com](https://forum.omz-software.com/topic/3288/ctypes-pythonapi-version/4)_

[@ywangd](https://forum.omz-software.com/user/ywangd) That's a `unicode`/`str`/`bytes` issue. Short answer, the arguments to Python's C API need to be byte strings (`b"..."`) unless stated otherwise in the docs. Long explanation below. `:)`

In C, the type `char` represents a byte (which is generally agreed to be 8 bits nowadays). Most code uses `char *` (a pointer to a `char`, which is effectively used as an array of unknown size) as the data type for "strings". Because a `char` is only 8 bit wide, it can't hold a full Unicode code point. There is the `wchar_t` data type, which is not really standardized either, but it's wider than `char` and can usually hold a Unicode code point, so APIs that support Unicode properly use `wchar_t *` instead of `char *` for strings.

In Python 2, the situation is similar. `str` is like C's `char *` \- it's made of 8-bit bytes and can't hold Unicode text properly, and `unicode` is like C's `wchar_t *` and supports full Unicode. That's why `ctypes` converts `str` to `char *` and `unicode` to `wchar_t *` and vice versa.

Now Python 3 comes along and cleans up a lot of Python 2's Unicode issues. In Python 3, you have the two data types `bytes` and `str`. Python 3's `bytes` is an 8-bit string like Python 2's `str`, and Python 3's `str` is a Unicode string like Python 2's `unicode`. And most importantly, in both Python versions the string `"hello"` is of type `str`, which means that under Python 2 it's 8-bit (i. e. `char *`) and under Python 3 it's Unicode (i. e. `wchar_t *`).

Python's C API functions, such as `PyRun_SimpleString` use normal `char *` for source code. So under Python 2, your code works fine - `"print(42)"` is an 8-bit string, gets converted to `char *`, which is what `PyRun_SimpleString` wants. Perfect. Under Python 3, `"print(42)"` is a Unicode string, which gets converted to `wchar_t *`, and then things go wrong. Because `wchar_t` is 32 bits wide under iOS, the text `print(42)` represented as a `wchar_t *` has three null bytes between each character (which would be used if the character had a higher code point in Unicode). Null bytes are also the "end of string" marker in C. Python reads the start of the `wchar_t *` string, but expects a `char *` \- it sees a `p`, then a null byte, and thinks "great, I'm done" and so it just runs `p` instead of `print(42)`.
