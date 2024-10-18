import re
import random

easy_d = [
    "the quick brown fox jumps over the lazy dog",
    "a stitch in time saves nine",
    "actions speak louder than words"
]

medium_d = [
    "My name is Walter Hartwell White. I live at 308 Negra Aroya Lane, Albuquerque, New Mexico, 87104.",
    "Life is either a daring adventure or nothing at all",
    "You miss 100 percent of the shots you dont take"
]

hard_d = [
    # lorem ipsum text
    "liqu3t urn@ nec libero fermentum, in interdum justo convallis. Mauris vite purus m3lu, ultrice$ metu$ id, con$eqat0 odio.",
    "cras ultrices tincidunt erat, eget vehicula lectus molestie id. In hac habitasse platea dictumst. Sed gravida tristique justo.",
]

freestyle_d = ["This is freestyle mode; type whatever comes to your mind."]

easy = random.choice(easy_d)
medium = random.choice(medium_d)
hard = random.choice(hard_d)

freestyle_words = [
    random.choice(re.findall(r'\b\w+\b', passage))
    for passage in [easy, medium]
    for _ in range(30)
]
freestyle = ' '.join(freestyle_words)
