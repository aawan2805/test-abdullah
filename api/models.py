from django.db import models

# Create your models here.
class Company(models.Model):
	title = models.CharField(max_length=50)
	inspectorName = models.CharField(max_length=50)
	itemsOk = models.IntegerField()
	issuesWarningCount = models.IntegerField()
	issuesCriticalCount = models.IntegerField()
	company = models.CharField(max_length=50)

	class Meta:
		db_table = 'company'

