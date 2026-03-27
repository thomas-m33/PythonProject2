from django.core.exceptions import ValidationError

class ContainsCapOrNumValidator:
    def validate(self, password, user=None):
        contains = False
        for char in password:
            if char.isupper() or char.isdigit(): # checks to see if char is a capital letter or number
                contains = True
                break
        if not contains:
            raise ValidationError(
                "Your password must contain at least one number or capital letter",
                code="password_no_capital_letter_or_number",
            )

    def get_help_text(self):
        return "Your password must contain at least one number or capital letter."