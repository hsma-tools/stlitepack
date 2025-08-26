from stlitepack import pack

def test_pack_single_page_extra_file_toml_EMBED():
    pack("tests/single_page_extra_file/simple_with_config.py",
         output_dir="tests/single_page_extra_file/with_config_embed/docs",
         use_raw_api=False,
         extra_files_to_embed=["tests/single_page_extra_file/.streamlit/config.toml"]
         )

def test_pack_single_page_extra_file_toml_EMBED_raw_api():
    pack("tests/single_page_extra_file/simple_with_config.py",
         output_dir="tests/single_page_extra_file/with_config_raw_api_embed/docs",
         use_raw_api=True,
         extra_files_to_embed=["tests/single_page_extra_file/.streamlit/config.toml"]
         )

# We expect this to not work as the basic API cannot link files
def test_pack_single_page_reqs_file_toml_LINK():
    pack("tests/single_page_extra_file/simple_with_config.py",
         output_dir="tests/single_page_extra_file/with_config_link/docs",
         use_raw_api=False,
        extra_files_to_link=["tests/single_page_extra_file/.streamlit/config.toml"]
         )

# This *should* work - not sure why it isn't
def test_pack_single_page_reqs_file_toml_LINK_raw_api():
    pack("tests/single_page_extra_file/simple_with_config.py",
         output_dir="tests/single_page_extra_file/with_config_raw_api_link/docs",
         use_raw_api=True,
        extra_files_to_link=["tests/single_page_extra_file/.streamlit/config.toml"]
         )
