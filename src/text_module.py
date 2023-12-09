import re
import random

easy = """python is python is"""
medium = """My name is Walter Hartwell White. I live at 308 Negra Aroya Lane, Albuquerque, New Mexico, 87104."""
hard = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderi"""

freestyle = ' '.join(random.choice(re.findall(r'\b\w+\b', medium)) for _ in range(10))
