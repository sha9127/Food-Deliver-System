from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, email, password, name, address, role):
        if not email:
            raise ValueError('Email is required!')
        user = self.model(email=self.normalize_email(email),
                          name=name, address=address, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
