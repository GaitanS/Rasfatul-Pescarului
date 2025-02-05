from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Include user's profile.is_email_verified status in the token hash
        # This ensures the token becomes invalid once email is verified
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.is_email_verified)
        )

email_verification_token = EmailVerificationTokenGenerator()
