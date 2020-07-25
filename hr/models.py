# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Messages(models.Model):
    emp_no = models.IntegerField(primary_key=True)
    amount = models.BigIntegerField()
    due_date = models.DateField(blank=True, null=True)
    fiscal_code = models.CharField(max_length=45, blank=True, null=True)
    invalid_after_due_date = models.CharField(max_length=5)
    markdown = models.CharField(max_length=65, blank=True, null=True)
    notice_number = models.BigIntegerField()
    subject = models.CharField(max_length=44)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'messages'
