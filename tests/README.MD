Tests currently don't really check the resulting apps work - only that the function to build the apps works.
Manual checking is then done of the resulting html files via the 'tests' page in the documentation, which links out automatically on render to all outputs generated using pytest.

# Additional tests to write

- Check functions fail if v<0.76.0 is passed
