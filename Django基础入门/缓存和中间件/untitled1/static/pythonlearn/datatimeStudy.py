import os
from datetime import datetime

print(datetime.now().strftime("%Y/%m/%d"))

str = "lala/dadada/pppp"

print(os.path.split(str))