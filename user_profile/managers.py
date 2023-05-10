from django.db.models import Manager, Count

class GraphManager(Manager):

    def total_value(self, user):
        total_value = self.get_queryset().filter(add__owner=user).values('created_at__date').annotate(total=Count('id')).values('created_at__date', "total").order_by('created_at__date')
        return total_value
    

class GraphDetailManager(Manager):

    def total_value_detail(self, add):
        v = self.get_queryset().filter(add=add).values('created_at__date').annotate(total=Count('id')).values('created_at__date', "total").order_by('created_at__date')
        return v