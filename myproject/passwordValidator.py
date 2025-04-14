from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        # check letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least 1 uppercase letter."),
                code='password_no_upper',
            )
        # check digit
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("Password must contain at least 1 digit."),
                code='password_no_digit',
            )
        # symbol check
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError(
                _("Password must contain at least 1 symbol.(@#$%^&+=)"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Password must contain at least 1 uppercase letter ,1 symbol and 1 digit.")