import re

original_string = r"D:\PROJECTS\glucoma_detect\glucoma_detect\website"

# Use regular expressions to remove the last 8 words
result_string = re.sub(r'(\\[^\\]+){8}$', '', original_string)

print(result_string)