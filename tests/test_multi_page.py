from stlitepack import pack


def test_pack_simplest_multipage_pages_subfolder():
    pack(
        "tests/multi_page_pages_subfolder_no_reqs/simplest.py",
        output_dir="tests/multi_page_pages_subfolder_no_reqs/simple_api/docs",
        requirements=None,
    )


def test_pack_simplest_multipage_pages_subfolder_raw():
    pack(
        "tests/multi_page_pages_subfolder_no_reqs/simplest.py",
        output_dir="tests/multi_page_pages_subfolder_no_reqs/raw_api/docs",
        requirements=None,
        use_raw_api=True,
    )
