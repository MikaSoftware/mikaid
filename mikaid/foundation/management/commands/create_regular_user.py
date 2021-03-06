# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from starterkit.utils import (
    get_random_string,
    get_unique_username_from_email
)
from foundation import constants
from foundation.models import User


class Command(BaseCommand):
    help = _('Command will create an admin account.')

    def add_arguments(self, parser):
        """
        Run manually in console:
        python manage.py create_regular_user 0 "bart+regular@mikasoftware.com" "123password" "Bart" "Mika";
        """
        parser.add_argument('tenant_id', nargs='+', type=int)
        parser.add_argument('email', nargs='+', type=str)
        parser.add_argument('password', nargs='+', type=str)
        parser.add_argument('first_name', nargs='+', type=str)
        parser.add_argument('last_name', nargs='+', type=str)

    def handle(self, *args, **options):
        # Get the user inputs.
        tenant_id = options['tenant_id'][0]
        email = options['email'][0]
        password = options['password'][0]
        first_name = options['first_name'][0]
        last_name = options['last_name'][0]

        # Defensive Code: Prevent continuing if the email already exists.
        if User.objects.filter(email=email, tenant_id=tenant_id).exists():
            raise CommandError(_('Email already exists, please pick another email.'))

        # Create the user.
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
            is_superuser=False,
            is_staff=False,
            was_email_activated=True,
            tenant_id=tenant_id
        )

        # Generate and assign the password.
        user.set_password(password)
        user.save()

        # For debugging purposes.
        self.stdout.write(
            self.style.SUCCESS(_('Successfully created a shared account.'))
        )
