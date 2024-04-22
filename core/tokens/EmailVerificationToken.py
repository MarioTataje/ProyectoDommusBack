from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, usuario, timestamp):
        return (
            six.text_type(usuario.idUsuario) + six.text_type(timestamp) +
            six.text_type(usuario.activo)
        )


account_activation_token = AccountActivationTokenGenerator()
