from django.test import TestCase

# Create your tests here.
import datetime

a = datetime.date(2022, 12, 12)
b = datetime.date(2022, 12,13)
print(int((a-b).days))