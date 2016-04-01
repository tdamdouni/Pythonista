// https://forum.omz-software.com/topic/1032/python-objective-c-bridge/2

//clipboardmodule.m

#import "Python.h"

PyObject* clipboard_get(PyObject* self, PyObject* pArgs)
{
    NSString *stringValue = [[UIPasteboard generalPasteboard] string];
    if (!stringValue) {
        return PyUnicode_FromString("");
    }
    return PyUnicode_FromString([stringValue UTF8String]);
}

static PyMethodDef clipboardMethods[] = {
    {"get", clipboard_get, METH_NOARGS, "get() -- Get the clipboard's text content as a string"},
    // [...]
    {NULL, NULL, 0, NULL} //sentinel
};

PyMODINIT_FUNC init_clipboard(void)
{
    Py_InitModule("_clipboard", clipboardMethods);
}