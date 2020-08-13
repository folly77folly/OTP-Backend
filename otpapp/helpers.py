from django.core.mail import send_mail
import random, string, datetime
from decouple import config




def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))