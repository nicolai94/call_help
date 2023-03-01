from crum import get_current_user
from django.db.models import Case, When, Q, F, Value, Count

from breaks import constants
from breaks.models.replacements import Replacement


class ReplacementFactory:
    model = Replacement

    def list(self):
        all_statuses = constants.BREAK_ALL_STATUSES
        annotates = dict()
        for status in all_statuses:
            annotates[f'{status}_pax'] = Count(
                    'breaks',
                    filter=Q(breaks__status=status),
                    distinct=True)

        qs = self.model.objects.prefetch_related(
            'group',
            'members',
            'members__employee',
            'members__employee__user'
        ).annotate(
            all_pax=Count('breaks', distinct=True),
        ).annotate(
            **annotates
        )
        return qs
