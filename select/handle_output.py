import StringIO
import sys

sys.stdout = buffer = StringIO()
print("Hello")
buffer.getvalue()