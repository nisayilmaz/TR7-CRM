import os
import re
from datetime import datetime
from django.db import models
# Create your models here.
from accounts.models import CustomUser
from crm.settings import EMAIL_HOST_USER
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

ROLES = (
    ('client', 'Son Kullanıcı'),
    ('partner', 'İş Ortağı'),
)

POC_REQUEST = (
    (1, 'Toplantı Aşaması'),
    (2, 'POC Talebi'),
    (3, 'POC Aşaması'),
    (4, 'POC Gerçekleştirildi'),
    (5, 'Yaklaşık Maliyet'),
    (6, 'Alım Aşaması'),
    (7, 'Pazarlık Aşaması'),
    (8, 'Gerçekleşti'),
    (9, 'Kapandı'),
    (10, 'Kaybedildi')
)

NOTES_CATEGORIES = (
    (1, 'Arama'),
    (2, 'Yüzyüze Görüşme'),
    (3, 'İş Ortağı İle Görüşme'),
    (4, 'E-posta'),
    (5, 'Genel'),
    (6, 'Etkinlik'),
    (7, 'İş Yemeği'),
    (8, 'Diğer'),
    (9, 'Online Görüşme'),
)


class Company(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=7, choices=ROLES)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    registered_by = models.ForeignKey(to=CustomUser, blank=True, null=True, on_delete=models.PROTECT)


class People(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=255)


class Project(models.Model):
    client = models.ForeignKey(to=Company, related_name="client", on_delete=models.CASCADE)
    partner = models.ForeignKey(to=Company, related_name="partner", on_delete=models.CASCADE, null=True, blank=True)
    registration_date = models.DateField()
    exp_end_date = models.DateField(null=True, blank=True)
    tender_date = models.DateField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    count = models.IntegerField()
    client_contact = models.ForeignKey(to=People, related_name="client_contact", on_delete=models.CASCADE, null=True, blank=True)
    partner_contact = models.ForeignKey(to=People, related_name="partner_contact", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    budget = models.FloatField()
    poc_request = models.CharField(max_length=1, choices=POC_REQUEST)
    probability = models.CharField(max_length=3)
    registered_by = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT)


class Notes(models.Model):
    note = models.TextField()
    creation_date = models.DateField(auto_now=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    category = models.CharField(max_length=1, choices=NOTES_CATEGORIES)



class FinishedProject(models.Model):
    invoice_date = models.DateField()
    invoice_amount = models.IntegerField()
    end_date = models.DateField(default=datetime.now, blank=True)
    client = models.ForeignKey(to=Company, related_name="finished_client", on_delete=models.CASCADE)
    partner = models.ForeignKey(to=Company, related_name="finished_partner", on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    budget = models.FloatField()
    count = models.IntegerField()
    registered_by = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT)

class FileModel(models.Model):
    project = models.ForeignKey(FinishedProject, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='sozlesmeler/', null=True, blank=True)




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    url = instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))
    postfix = "/#/password_reset/"
    if os.getenv("DEVELOPMENT_MODE", "False") == "True":
        url = re.match(r'.*(?=5000/api/auth/password_reset)', url).group() + "5050"
    else:
        url = re.match(r'.*(?=/api/auth/password_reset)', url).group()
    email_plaintext_message = url + postfix + "{}".format(
            reset_password_token.key)

    message = '''TR7 CRM şifrenizi sıfırlamak için aşağıdaki linke tıklayınız.\n\n\nLink : {link}'''.format(link=email_plaintext_message)
    send_mail(
        # title:
        "TR7 CRM İçin Şifre Sıfırlama Maili",
        # message:
        message,
        # from:
        EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )