from django.test import TestCase
import re

email_pattern = r"email\s*/\s*([^<>@\s]+@[^<>@\s]+\.[^<>@\s]+)"

# text = "email / hslfj@gmail.com"
text = "email / another@example.com email / ano33ther@example.com"


match = re.search( email_pattern , text )

if match : 
    print( match.groups(2))


