from django.core.exceptions import ValidationError

class ContainsNumberValidator:
    def validate(self, password, user=None):
        has_num = False
        for char in password:
            if char.isdigit(): # checks to see if the password has a number
                has_num = True
                break
        if not has_num: # if there is no number, tell the user they need one in their password
            raise ValidationError(
                "Your password must contain at least one number.",
                code="password_no_number",
            )

    def get_help_text(self): # displays the return message to user as a password requirement
        return "Your password must contain at least one number."

class ContainsCapitalLetterValidator:
    def validate(self, password, user=None):
        has_cap_letter = False
        for char in password:
            if char.isupper(): # checks to see if char is a capital letter
                has_cap_letter = True
                break
        if not has_cap_letter:
            raise ValidationError(
                "Your password must contain at least one capital letter.",
                code="password_no_capital_letter",
            )

    def get_help_text(self):
        return "Your password must contain at least one capital letter."

# The risk of SQL injection attacks in the login/register forms is low because Django treats the user input strictly as text