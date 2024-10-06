from django.db import models
from django.utils.timezone import now
from tailored_feed.models.user import User

class Assessment(models.Model):
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assessment_owner")
    creationDate = models.DateTimeField(default=now, editable=False)


    def to_dict(self):

        return {
            'id': self.id,
            'name': self.name,
            'owner': {
                'id': self.owner.id,
                'username': self.owner.username,
                'email': self.owner.email
            },
            'creationDate': self.creationDate.isoformat(),
        }