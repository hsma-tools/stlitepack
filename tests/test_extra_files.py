from stlitepack import pack

def test_pack_single_page_reqs_file():
    pack("tests/single_page_extra_file/simple_with_config.py",
         output_dir="tests/single_page_extra_file/with_config/docs",
         extra_files=["tests/single_page_extra_file/.streamlit/config.toml"]
         )

def test_pack_single_page_reqs_file_raw_api():
    pack("tests/single_page_extra_file/simple_with_config.py",
         output_dir="tests/single_page_extra_file/with_config_raw_api/docs",
         use_raw_api=True,
         extra_files=["tests/single_page_extra_file/.streamlit/config.toml"]
         )
