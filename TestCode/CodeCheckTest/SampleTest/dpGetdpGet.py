import re

def contains_consecutive_dpSet(text):
    # Define the pattern for consecutive dpSet* calls including newlines
    pattern = r'dpSet\w*\(\s*[\s\S]*?dpSet\w*\('
    # Search for consecutive "dpSet*(" calls in the given text
    return re.search(pattern, text) is not None

# Example usage
text = """
This is a test string.
dpSet("config1", value1);
dpSet("config2", value2);

Another line without the pattern.
dpGet("test", value);
dpSet("config3", value3);
"""

if contains_consecutive_dpSet(text):
    print("The string contains consecutive 'dpSet*(' calls.")
else:
    print("The string does not contain consecutive 'dpSet*(' calls.")
