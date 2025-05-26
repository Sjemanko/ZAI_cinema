from rest_framework.relations import PrimaryKeyRelatedField


class CustomSeatField(PrimaryKeyRelatedField):
    default_error_messages = {
        'does_not_exist': 'To miejsce nie istnieje.',
        'incorrect_type': 'Błędny typ – oczekiwano ID.'
    }
