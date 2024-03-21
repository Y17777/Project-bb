from django_filters import FilterSet

from bbapp.models import Comment, Bullets


class CommentFilterSet(FilterSet):
    class Meta:
        model = Comment
        fields = [
            'commentPost'
        ]

        def __init__(self, *args, **kwargs):
            super(CommentFilterSet, self).__init__(*args, **kwargs)
            self.fields['commentPost'].queryset = Bullets.objects.filter(author_id=kwargs['request'])
