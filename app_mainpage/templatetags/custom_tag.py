from django import template

register = template.Library()

'''created for filter users viewing (by group)'''
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
