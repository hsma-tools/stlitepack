from stlitepack import pack

def test_pack_simples():
    pack("tests/simplest/simplest.py", output_dir="tests/simplest/docs", requirements=None)
