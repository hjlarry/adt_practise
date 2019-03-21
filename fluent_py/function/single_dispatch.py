from functools import singledispatch
from collections import abc
import numbers
import html


@singledispatch
def htmlize(obj):
    content = html.escape(repr(obj))
    return f"<pre>{content}</pre>"


@htmlize.register(str)
def _(text):
    content = html.escape(text).replace("\n", "<br>\n")
    return f"<p>{content}</p>"


@htmlize.register(numbers.Integral)
def _(n):
    return f"<pre>{n} (0x{n:x})</pre>"


@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>"


print(htmlize({1, 2, 3}))
print(htmlize(abs))
print(htmlize(42))
print(htmlize("Heimlich & Co. \n- a game"))
print(htmlize(["alpha", 66, {3, 2, 2}]))
