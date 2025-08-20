from stlitepack import setup_github_pages
from stlitepack.publish import _create_nojekyll, _create_workflow


def test_nojekyll_creation():
    _create_nojekyll(output_dir="tests/workflow_file_creation")

def test_workflow_generation():
    _create_workflow(print_only=True)

def test_workflow_file_creation():
    _create_workflow(print_only=False, use_docs=False)

def test_workflow_setup_helper():
    setup_github_pages()

def test_workflow_setup_helper_main_message():
    setup_github_pages(mode="manual")

def test_workflow_setup_helper_main_message_use_docs():
    setup_github_pages(mode="manual", use_docs=True)
