"""
Extra tests.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_extra_001():
    """
    Test a totally blank input.
    """

    # Arrange
    source_markdown = ""
    expected_tokens = ["[BLANK(1,1):]"]
    expected_gfm = ""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_002():
    """
    Test a blank input with only whitespace.
    """

    # Arrange
    source_markdown = "   "
    expected_tokens = ["[BLANK(1,1):   ]"]
    expected_gfm = ""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_003():
    """
    Test to make sure the wide range of characters meets the GRM/CommonMark encodings.
    Note that since % is not followed by a 2 digit hex value, it is encoded per
    the common mark libraries.
    """

    # Arrange
    source_markdown = "[link](!\"#$%&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~)"
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:!%22#$%25&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + "%5E_%60a-z%7B%7C%7D~::!\"#$%&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        "<p><a href=\"!%22#$%25&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + '%5E_%60a-z%7B%7C%7D~">link</a></p>'
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_004():
    """
    Test to make sure the wide range of characters meets the GRM/CommonMark encodings.
    Note that since % is followed by a 2 digit hex value, it is encoded per the common
    mark libraries except for the % and the 2 digit hex value following it.

    Another example of this is example 511:
    https://github.github.com/gfm/#example-511
    """

    # Arrange
    source_markdown = (
        "[link](!\"#$%12&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~)"
    )
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:!%22#$%12&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + "%5E_%60a-z%7B%7C%7D~::!\"#$%12&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        "<p><a href=\"!%22#$%12&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + '%5E_%60a-z%7B%7C%7D~">link</a></p>'
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_005():
    """
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
    """

    # Arrange
    source_markdown = "[link](http://google.com/search%)"
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:http://google.com/search%25::http://google.com/search%:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = '<p><a href="http://google.com/search%25">link</a></p>'

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_006():
    """
    lists and fenced code blocks within a block quote
    """

    # Arrange
    source_markdown = """> + list
> ```block
> A code block
> ```
> 1. another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(2,3):`:3:block:::::]",
        "[text(3,3):A code block:]",
        "[end-fcode-block::3:False]",
        "[olist(5,3):.:1:5:]",
        "[para(5,6):]",
        "[text(5,6):another list:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<ol>
<li>another list</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007a():
    """
    Text and a link reference definition within a block quote.
    """

    # Arrange
    source_markdown = """> this is text
> [a not so
>  simple](/link
> "a title")
>   a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n\n  ]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a title::::a not so\nsimple:False:"::\n:]',
        "[text(2,4):a not so\nsimple::\n]",
        "[end-link::]",
        "[text(4,13):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a title">a not so
simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007b():
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a not
>  so simple](/link
> "a
>  title"
>  )
> a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a not\nso simple:False:"::\n:\n]',
        "[text(2,4):a not\nso simple::\n]",
        "[end-link::]",
        "[text(6,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007cx():
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a\a
>  not
>  so simple](/link
> "a
>  title"
>  )
> a real test
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a \nnot\nso simple:False:"::\n:\n]',
        "[text(2,4):a\nnot\nso simple:: \n\n]",
        "[end-link::]",
        "[text(7,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a
not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007ca():
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a
>  not\a
>  so simple](/link
> "a
>  title"
>  )
> a real test
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a\nnot \nso simple:False:"::\n:\n]',
        "[text(2,4):a\nnot\nso simple::\n \n]",
        "[end-link::]",
        "[text(7,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a
not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007d():
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a
>  not
>  so simple](/link
> "a
>  title"
>  )
> a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a\nnot\nso simple:False:"::\n:\n]',
        "[text(2,4):a\nnot\nso simple::\n\n]",
        "[end-link::]",
        "[text(7,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a
not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007e():
    """
    Almost looks like a fenced code block, but is really a code span.
    """

    # Arrange
    source_markdown = """> this is text
> ``
> foo
> bar  
> baz
> ``
> a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n\n\n\n\n]",
        "[text(1,3):this is text\n::\n]",
        "[icode-span(2,3):foo\a\n\a \abar  \a\n\a \abaz:``:\a\n\a \a:\a\n\a \a]",
        "[text(6,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<code>foo bar   baz</code>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_008x():
    """
    Simple unordered list with increasing indent in a block quote.
    """

    # Arrange
    source_markdown = """> * this is level 1
>   * this is level 2
>     * this is level 3
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):*::4:]",
        "[para(1,5):]",
        "[text(1,5):this is level 1:]",
        "[end-para:::True]",
        "[ulist(2,5):*::6:  ]",
        "[para(2,7):]",
        "[text(2,7):this is level 2:]",
        "[end-para:::True]",
        "[ulist(3,7):*::8:    ]",
        "[para(3,9):]",
        "[text(3,9):this is level 3:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>this is level 1
<ul>
<li>this is level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_008a():
    """
    Variation on 8 with no block quote.
    """

    # Arrange
    source_markdown = """* this is level 1
  * this is level 2
    * this is level 3
"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):this is level 1:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):this is level 2:]",
        "[end-para:::True]",
        "[ulist(3,5):*::6:    ]",
        "[para(3,7):]",
        "[text(3,7):this is level 3:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>this is level 1
<ul>
<li>this is level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009():
    """
    Simple block quote within an unordered list.
    """

    # Arrange
    source_markdown = """- > This is one section of a block quote
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[block-quote(1,3):  :  > \n]",
        "[para(1,5):]",
        "[text(1,5):This is one section of a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>This is one section of a block quote</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009a():
    """
    Simple block quote within an ordered list.
    """

    # Arrange
    source_markdown = """1. > This is one section of a block quote
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n]",
        "[para(1,6):]",
        "[text(1,6):This is one section of a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>This is one section of a block quote</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009b():
    """
    Simple block quote within an ordered list.
    """

    # Arrange
    source_markdown = """1.
   > This is one section of a block quote
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   > \n]",
        "[para(2,6):]",
        "[text(2,6):This is one section of a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>This is one section of a block quote</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009c():
    """
    Simple block quote within an ordered list.
    """

    # Arrange
    source_markdown = """1. > This is one section of a block quote
   > Just one section.
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n]",
        "[para(1,6):\n]",
        "[text(1,6):This is one section of a block quote\nJust one section.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>This is one section of a block quote
Just one section.</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_010x():
    """
    List item with weird progression.
    """

    # Arrange
    source_markdown = """* First Item
  * First-First
   * First-Second
    * First-Third
* Second Item
"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):First Item:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):First-First:]",
        "[end-para:::True]",
        "[li(3,4):5:   :]",
        "[para(3,6):]",
        "[text(3,6):First-Second:]",
        "[end-para:::True]",
        "[li(4,5):6:    :]",
        "[para(4,7):]",
        "[text(4,7):First-Third:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):Second Item:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>First Item
<ul>
<li>First-First</li>
<li>First-Second</li>
<li>First-Third</li>
</ul>
</li>
<li>Second Item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_010a():
    """
    List item with weird progression.
    """

    # Arrange
    source_markdown = """* First Item
 * Second Item    
  * Third Item
"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):First Item:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4)::    ]",
        "[text(2,4):Second Item:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):Third Item:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>First Item</li>
<li>Second Item</li>
<li>Third Item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_010b():
    """
    List item with weird progression.
    """

    # Arrange
    source_markdown = """1. First Item
   1. First-First
    1. First-Second
     1. First-Third
      1. First-Four
1. Second Item
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):First Item:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):First-First:]",
        "[end-para:::True]",
        "[li(3,5):7:    :1]",
        "[para(3,8):]",
        "[text(3,8):First-Second:]",
        "[end-para:::True]",
        "[li(4,6):8:     :1]",
        "[para(4,9):]",
        "[text(4,9):First-Third:]",
        "[end-para:::True]",
        "[li(5,7):9:      :1]",
        "[para(5,10):]",
        "[text(5,10):First-Four:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(6,1):3::1]",
        "[para(6,4):]",
        "[text(6,4):Second Item:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>First Item
<ol>
<li>First-First</li>
<li>First-Second</li>
<li>First-Third</li>
<li>First-Four</li>
</ol>
</li>
<li>Second Item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_011x():
    """
    Block quote followed directly by Atx Heading.
    """

    # Arrange
    source_markdown = """> simple text
> dd
> dd
# a
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):simple text\ndd\ndd::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(4,1):1:0:]",
        "[text(4,3):a: ]",
        "[end-atx::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>simple text
dd
dd</p>
</blockquote>
<h1>a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_011a():
    """
    Variation of 11 with no newline after Atx Heading
    """

    # Arrange
    source_markdown = """> simple text
> dd
> dd
# a"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):simple text\ndd\ndd::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(4,1):1:0:]",
        "[text(4,3):a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<blockquote>
<p>simple text
dd
dd</p>
</blockquote>
<h1>a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_011b():
    """
    Variation of 11 with newline after Block Quote and before Atx Heading
    """

    # Arrange
    source_markdown = """> simple text
> dd
> dd

# a"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):\n\n]",
        "[text(1,3):simple text\ndd\ndd::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[atx(5,1):1:0:]",
        "[text(5,3):a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<blockquote>
<p>simple text
dd
dd</p>
</blockquote>
<h1>a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_012():
    """
    Unordered lists, nested within each other with weird indents.
    """

    # Arrange
    source_markdown = """This is a test

 * this is level 1
 * this is also level 1
   * this is level 2
   * this is also level 2
      * this is level 3
   * this is also level 2
    * this is also level 2
    * this is also level 2
* this is also level 1
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a test:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[ulist(3,2):*::3: ]",
        "[para(3,4):]",
        "[text(3,4):this is level 1:]",
        "[end-para:::True]",
        "[li(4,2):3: :]",
        "[para(4,4):]",
        "[text(4,4):this is also level 1:]",
        "[end-para:::True]",
        "[ulist(5,4):*::5:   ]",
        "[para(5,6):]",
        "[text(5,6):this is level 2:]",
        "[end-para:::True]",
        "[li(6,4):5:   :]",
        "[para(6,6):]",
        "[text(6,6):this is also level 2:]",
        "[end-para:::True]",
        "[ulist(7,7):*::8:      ]",
        "[para(7,9):]",
        "[text(7,9):this is level 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(8,4):5:   :]",
        "[para(8,6):]",
        "[text(8,6):this is also level 2:]",
        "[end-para:::True]",
        "[li(9,5):6:    :]",
        "[para(9,7):]",
        "[text(9,7):this is also level 2:]",
        "[end-para:::True]",
        "[li(10,5):6:    :]",
        "[para(10,7):]",
        "[text(10,7):this is also level 2:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(11,1):2::]",
        "[para(11,3):]",
        "[text(11,3):this is also level 1:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<p>This is a test</p>
<ul>
<li>this is level 1</li>
<li>this is also level 1
<ul>
<li>this is level 2</li>
<li>this is also level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
<li>this is also level 2</li>
<li>this is also level 2</li>
<li>this is also level 2</li>
</ul>
</li>
<li>this is also level 1</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_013x():
    """
    Paragraph followed by a blank line and a SetExt heading in a block quote
    """

    # Arrange
    source_markdown = """ > this is text
 >
 > a setext heading
 > that is not properly
>  indented
> ---
"""
    expected_tokens = [
        "[block-quote(1,2): : > \n >\n > \n > \n> \n> \n]",
        "[para(1,4):]",
        "[text(1,4):this is text:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[setext(6,3):-:3::(3,4)]",
        "[text(3,4):a setext heading\nthat is not properly\nindented::\n\n \x02]",
        "[end-setext::]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text</p>
<h2>a setext heading
that is not properly
indented</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_013a():
    """
    Variation of 13x without the block quote.
    """

    # Arrange
    source_markdown = """this is text

a setext heading
that is not properly
 indented
---
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is text:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[setext(6,1):-:3::(3,1)]",
        "[text(3,1):a setext heading\nthat is not properly\nindented::\n\n \x02]",
        "[end-setext::]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<p>this is text</p>
<h2>a setext heading
that is not properly
indented</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014x():
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    *****
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):\n   ]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(3,6):*:   :*****]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<hr />
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_014a():
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break_misaligned
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>     *****
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):\n   \n    ]",
        "[text(1,6):list\nthis\n::\n\n]",
        "[text(3,5):*****:]",
        "[end-para:::True]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<hr />
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014bx():
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """> 1. *****
>    list
>    this
>    *****
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[tbreak(1,6):*::*****]",
        "[para(2,6):   \n   ]",
        "[text(2,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,6):*:   :*****]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<hr />
list
this
<hr />
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014ba():
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """1. *****
   list
   this
   *****
1. that

"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[tbreak(1,4):*::*****]",
        "[para(2,4):\n]",
        "[text(2,4):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,4):*::*****]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<hr />
list
this
<hr />
</li>
<li>that</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014bb():
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """> *****
> list
> this
> *****
> that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[tbreak(1,3):*::*****]",
        "[para(2,3):\n]",
        "[text(2,3):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,3):*::*****]",
        "[para(5,3):]",
        "[text(5,3):that:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<hr />
<p>list
this</p>
<hr />
<p>that</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_015():
    """
    TBD - test_md027_good_block_quote_ordered_list_atx_heading
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    # Heading
> 1. that

"""
    expected_tokens = []
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<h1>Heading</h1>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_016():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    Heading
>    ---
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> ]",
        "[olist(1,3):.:1:5:  ]",
        "[para(1,6):\n   ]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[setext(5,6):-:3:   :(4,6)]",
        "[text(4,6):Heading:]",
        "[end-setext:   :]",
        "[li(6,3):5:  :1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
<h2>Heading</h2>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_017():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>        indented
>        code block
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> ]",
        "[olist(1,3):.:1:5:  ]",
        "[para(1,6):\n   ]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[icode-block(4,7):    :\n    ]",
        "[text(4,7):indented\n   code block:   ]",
        "[end-icode-block:::True]",
        "[li(6,3):5:  :1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
<pre><code>indented
code block
</code></pre>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_018():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    ```html
>    <html>
>    ```
> 1. that
"""
    expected_tokens = []
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<pre><code class="language-html">&lt;html&gt;
</code></pre>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_019():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    <!-- this is a comment -->
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5:  ]",
        "[para(1,6):\n   ]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,3)]",
        "[text(3,6):<!-- this is a comment -->:   ]",
        "[end-html-block:::False]",
        "[olist(4,3):.:1:5:  ]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<!-- this is a comment -->
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_020():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    [abc]: /url
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n]",
        "[olist(1,3):.:1:5:  ]",
        "[para(1,6):\n   ]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[link-ref-def(4,6):True:   :abc:: :/url:::::]",
        "[li(5,3):5:  :1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_021():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item 1
   1. Item 1a
  100. Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):Item 1a:]",
        "[end-para:::True]",
        "[li(3,3):7:  :100]",
        "[para(3,8):]",
        "[text(3,8):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
</ol>
</li>
<li>Item 1b</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_021a():
    """
    TBD
    """

    # Arrange
    source_markdown = """* Item 1
  * Item 1a
 * Item 2
   * Item 2a
"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):Item 1:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):Item 1a:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,2):3: :]",
        "[para(3,4):]",
        "[text(3,4):Item 2:]",
        "[end-para:::True]",
        "[ulist(4,4):*::5:   ]",
        "[para(4,6):]",
        "[text(4,6):Item 2a:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Item 1
<ul>
<li>Item 1a</li>
</ul>
</li>
<li>Item 2
<ul>
<li>Item 2a</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_021b():
    """
    TBD
    """

    # Arrange
    source_markdown = """>  + list
>    this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,4):+::5: ]",
        "[para(1,6):\n   ]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_021c():
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a test

>  * this is level 1
>    * this is level 2
>      * this is level 3
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a test:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> \n> ]",
        "[ulist(3,4):*::5: ]",
        "[para(3,6):]",
        "[text(3,6):this is level 1:]",
        "[end-para:::True]",
        "[ulist(4,6):*::7:   ]",
        "[para(4,8):]",
        "[text(4,8):this is level 2:]",
        "[end-para:::True]",
        "[ulist(5,8):*::9:     ]",
        "[para(5,10):]",
        "[text(5,10):this is level 3:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>This is a test</p>
<blockquote>
<ul>
<li>this is level 1
<ul>
<li>this is level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
