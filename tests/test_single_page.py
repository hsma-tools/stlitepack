from stlitepack import pack


def test_pack_single_page_reqs_file():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_file/docs",
        requirements="tests/single_page_with_reqs/requirements.txt",
    )


def test_pack_single_page_reqs_list():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_list/docs",
        requirements=["streamlit", "pandas", "numpy", "plotly", "matplotlib"],
    )


def test_pack_single_page_reqs_file_versioned_strict():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_file_strict/docs",
        requirements="tests/single_page_with_reqs/requirements_strict.txt",
    )


def test_pack_single_page_reqs_file_versioned_loose():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_file_loose/docs",
        requirements="tests/single_page_with_reqs/requirements_loose.txt",
    )


def test_pack_single_page_reqs_file_raw_api():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_file_raw_api/docs",
        requirements="tests/single_page_with_reqs/requirements.txt",
        use_raw_api=True,
    )


def test_pack_single_page_reqs_list_raw_api():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_list_raw_api/docs",
        requirements=["streamlit", "pandas", "numpy", "plotly", "matplotlib"],
        use_raw_api=True,
    )


def test_pack_single_page_reqs_file_versioned_strict_raw_api():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_file_strict_raw_api/docs",
        requirements="tests/single_page_with_reqs/requirements_strict.txt",
        use_raw_api=True,
    )


def test_pack_single_page_reqs_file_versioned_loose_raw_api():
    pack(
        "tests/single_page_with_reqs/single_page_with_reqs.py",
        output_dir="tests/single_page_with_reqs/from_reqs_file_loose_raw_api/docs",
        requirements="tests/single_page_with_reqs/requirements_loose.txt",
        use_raw_api=True,
    )
