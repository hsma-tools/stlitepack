from stlitepack import pack


def test_pack_simplest():
    pack(
        "tests/simplest/simplest.py",
        output_dir="tests/simplest/docs",
        requirements=None,
    )


def test_pack_simplest_different_pyodide_version():
    pack(
        "tests/simplest/simplest.py",
        output_dir="tests/simplest_different_pyodide/docs",
        requirements=None,
        pyodide_version="0.27.0",
        use_raw_api=True,
    )
