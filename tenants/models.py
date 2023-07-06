from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Client(TenantMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Domain(DomainMixin):
    pass

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs:
# 		tenant = Client.objects.create(user=instance, schema_name= instance.username)
# 		tenant.save()
# 		domain = Domain()
# 		domain.domain = tenant.schema_name + ".global.localhost"
# 		domain.tenant = tenant 
# 		domain.is_primary = True
# 		domain.save()
		


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
