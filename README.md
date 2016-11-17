mbcserrors
==========

Error handlers for Windows MBCS encodings (`cp...`) provided by python.

- **mbcsbestfit**: Use ["best fit"][bestfitreadme] replacements for encoders.
 - **mbcsbestfitreplace**: Use Windows' replacement behavior.
 - **mbcsbestfitreplace**: Ignore unknown characters.
- **mbcsreplace**: Use Windows' replacement behavior for codecs.

[bestfitreadme]: http://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WindowsBestFit/readme.txt

Usage
-----

```Python
import mbcserrors

assert u'\u221e\ufffd'.encode('cp1252', errors='mbcsbestfitreplace') == b'8?'
assert u'\u221e\ufffd'.encode('cp1252', errors='mbcsbestfitignore') == b'8'
assert u'\u221e'.encode('cp1252', errors='mbcsbestfit') == b'8'
assert u'\u221e\ufffd'.encode('cp1252', errors='mbcsreplace') == b'??'

# throws the error for \ufffd back at you
# u'\u221e\ufffd'.encode('cp1252', errors='mbcsbestfit') == b'8'
```

Installation
------------

`setup.py` will pull some data and do the compilation.

Best fit files
--------------

A best fit file roughly corresponds to this structure:

```YAML
ast_ansi_file:
    codepage:    # key: cpnum
        cpinfo:
            bytes:
            encode_replace:
            decode_replace:
        mbtable: # decode
            sbcs:
                _length:
                single_mapping: list<[uint8_t -> wchar_t]>
            dbcs:
                _length:
                dbcs_range_unit: # single range units
                    start:
                    end:
                    tables:
                        _length: end - start + 1
                        single_mapping: [uint8_t -> wchar_t]
        wctable: # encode
            _length:
                single_mapping: [wchar_t -> (uint16_t if cpinfo.bytes == 2 else uint8_t)]
```

To generate a "best fit" table:

1.  Flatten `mbtable` into a single dict.
    1.  Copy all single-byte mappings into the dict.
    2.  For each element *trail* &rarr; *wchar* in the *i*-th table
        in each range unit, `mbtable[(unit_start + i) << 8 + trail] = wchar`.
2.  For each (*wchar*, *code*) pair in `wctable`, take the pair only if
    `mbtable[wctable[wchar]] != wchar` (non-roundtrip).

The replacement characters will be used for "replace" handlers.
