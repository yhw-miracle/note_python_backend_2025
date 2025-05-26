import os

def write_test_data(test_data, test_filepath = os.path.join(os.getcwd(), "tests", "result", "tests.md")):
    os.makedirs(os.path.dirname(test_filepath), exist_ok=True)
    with open(test_filepath, "a+", encoding="utf-8") as f:
        f.write("\n".join(test_data))
