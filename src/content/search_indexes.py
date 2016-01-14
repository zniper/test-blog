from haystack import indexes

from models import Entry


class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='title')
    text = indexes.CharField(document=True, use_template=True)
    categories = indexes.CharField()

    def get_model(self):
        return Entry

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_categories(self, obj):
        return obj.category_names
