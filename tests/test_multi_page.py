from stlitepack import pack

def test_pack_simplest_multipage_pages_subfolder():
    pack("tests/multi_page_pages_subfolder_no_reqs/simplest.py",
         output_dir="tests/multi_page_pages_subfolder_no_reqs/docs",
         requirements=None)
