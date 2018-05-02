from django.db.models.signals import post_save
from django.dispatch import receiver

from EnterpriseManagement import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        # 如果是jwt方式注册, 密码会比较短
        if not str(password).startswith('pbkdf2_sha256'):
            instance.set_password(password)
            instance.save()
