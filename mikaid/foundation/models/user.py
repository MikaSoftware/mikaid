# -*- coding: utf-8 -*-
"""user.py

The class model to represent the user in our application. This class overrides
default ``User`` model provided by ``Django`` to support the following:

TODO
"""
from __future__ import unicode_literals
from datetime import date, datetime, timedelta
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from starterkit.utils import (
    get_random_string,
    generate_hash
)
from foundation import constants


def get_expiry_date(days=2):
    """Returns the current date plus paramter number of days."""
    return timezone.now() + timedelta(days=days)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):  #TODO: UNIT TEST
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):  #TODO: UNIT TEST
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):  #TODO: UNIT TEST
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def delete_all(self):
        try:
            for user in User.objects.iterator(chunk_size=500):
                user.delete()
        except Exception as e:
            print(e)


class User(AbstractBaseUser, PermissionsMixin):

    #
    # SYSTEM UNIQUE IDENTIFIER
    #
    tenant_id = models.BigIntegerField(
        help_text=_('The tenant ID whom this user vault belongs to.'),
        blank=True,
        default=0,
        db_index=True,
    )
    email = models.EmailField( # THIS FIELD IS REQUIRED.
        _("Email"),
        help_text=_('Email address.'),
        db_index=True,
        unique=True
    )

    #
    # PERSON FIELDS - http://schema.org/Person
    #
    first_name = models.CharField(
        _("First Name"),
        max_length=63,
        help_text=_('The users given name.'),
        blank=True,
        null=True,
        db_index=True,
    )
    middle_name = models.CharField(
        _("Middle Name"),
        max_length=63,
        help_text=_('The users middle name.'),
        blank=True,
        null=True,
        db_index=True,
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=63,
        help_text=_('The users last name.'),
        blank=True,
        null=True,
        db_index=True,
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birthdate = models.DateField(
        _('Birthdate'),
        help_text=_('The users birthdate.'),
        blank=True,
        null=True
    )
    nationality = models.CharField(
        _("Nationality"),
        max_length=63,
        help_text=_('Nationality of the person.'),
        blank=True,
        null=True,
    )
    gender = models.CharField(
        _("Gender"),
        max_length=63,
        help_text=_('Gender of the person. While Male and Female may be used, text strings are also acceptable for people who do not identify as a binary gender.'),
        blank=True,
        null=True,
    )
    # profile = JSONField(
    #     _("Profile"),
    #     help_text=_('The user profile details.'),
    #     blank=True,
    #     null=True,
    # )

    #
    # SYSTEM FIELD
    #

    is_active = models.BooleanField(
        _('active'),
        default=True,
        blank=True
    )
    is_staff = models.BooleanField(
        _('Is Staff'),
        default=False,
        blank=True
    )
    is_superuser = models.BooleanField(
        _('Is Superuser'),
        default=False,
        blank=True
    )
    salt = models.CharField( #DEVELOPERS NOTE: Used for cryptographic signatures.
        _("Salt"),
        max_length=127,
        help_text=_('The unique salt value me with this object.'),
        default=generate_hash,
        unique=True,
        blank=True,
        null=True
    )
    type_of = models.PositiveSmallIntegerField(
        _("Type of"),
        help_text=_('The type of user this is. Value represents ID of user type.'),
        default=0,
        blank=True,
        db_index=True,
    )
    is_ok_to_email = models.BooleanField(
        _("Is OK to email"),
        help_text=_('Indicates whether customer allows being reached by email'),
        default=True,
        blank=True
    )
    is_ok_to_text = models.BooleanField(
        _("Is OK to text"),
        help_text=_('Indicates whether customer allows being reached by text.'),
        default=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)


    #
    # EMAIL ACTIVATION FIELD
    #

    was_email_activated = models.BooleanField(
        _("Was Email Activated"),
        help_text=_('Was the email address verified?'),
        default=False,
        blank=True
    )

    #
    # PASSWORD RESET FIELDS
    #

    pr_access_code = models.CharField(
        _("Password Reset Access Code"),
        max_length=127,
        help_text=_('The access code to enter the password reset page to be granted access to restart your password.'),
        blank=True,
        default=generate_hash,
    )
    pr_expiry_date = models.DateTimeField(
        _('Password Reset Access Code Expiry Date'),
        help_text=_('The date where the access code expires and no longer works.'),
        blank=True,
        default=get_expiry_date,
    )

    objects = UserManager()

    # DEVELOPERS NOTE:
    # WE WILL BE USING "EMAIL" AND "ACADEMY" AS THE UNIQUE PAIR THAT WILL
    # DETERMINE WHETHER THE AN ACCOUNT EXISTS. WE ARE DOING THIS TO SUPPORT
    # TENANT SPECIFIC USER ACCOUNTS WHICH DO NOT EXIST ON OTHER TENANTS.
    # WE USE CUSTOM "AUTHENTICATION BACKEND" TO SUPPORT THE LOGGING IN.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'is_staff',
        'is_active',
        'is_superuser',
        'tenant_id',
    ]

    class Meta:
        app_label = 'foundation'
        db_table = 'mika_users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        default_permissions = ()
        permissions = ()

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name  #TODO: UNIT TEST

    def __str__(self):
        return self.get_full_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)  #TODO: UNIT TEST

    def generate_pr_code(self):
        """
        Function generates a new password reset code and expiry date.
        """
        self.pr_access_code = get_random_string(length=127)
        self.pr_expiry_date = get_expiry_date()
        self.save()
        return self.pr_access_code

    def has_pr_code_expired(self):
        """
        Returns true or false depending on whether the password reset code
        has expired or not.
        """
        today = timezone.now()
        return today >= self.pr_expiry_date
