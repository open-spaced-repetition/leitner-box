# Contributing to leitner-box

Welcome to leitner-box!

In this short guide, you will get a quick overview of how you can contribute to the leitner-box project.

## Reporting issues

If you encounter an issue with leitner-box and would like to report it, you'll first want to make sure you're using the latest version of leitner-box.

The latest version of leitner-box can be found under [releases](https://github.com/open-spaced-repetition/leitner-box/releases) and you can verify the version of your current installation with the following command:
```
pip show leitner-box
```

Once you've confirmed your version, please report your issue in the [issues tab](https://github.com/open-spaced-repetition/leitner-box/issues).

## Contributing code

### Local setup

**Step 1**: Start by forking this repo, then cloning it to your local machine.

**Step 2**: Create a new local branch where you will implement your changes.

### Develop

Install the `leitner-box` python package locally in editable mode from the src with
```
pip install -e .
```

Now you're ready to make changes to `src/leitner_box` and see your changes reflected immediately!

### Test

leitner-box uses [pytest](https://docs.pytest.org) to run its tests. In order for your contribution to be accepted, your code must pass the tests.

You can install `pytest` with
```
pip install pytest
```

Run the tests with:
```
pytest
```

Additionally, you're encouraged to contribute your own tests to [tests/test_leitner_box.py](tests/test_leitner_box.py) to help make leitner_box more reliable!

### Submit a pull request

To submit a pull request, commit your local changes to your branch then push the branch to your fork. You can now open a pull request.