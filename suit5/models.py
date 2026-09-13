# No models here -- this module exists so Django's app loading imports suit5.config.
#
# config.py applies Suit5's global ModelAdmin defaults (actions at the bottom rather than
# the top, LIST_PER_PAGE) as import-time side effects. Nothing else imports it at startup,
# so it used to be pulled in lazily by the template tags -- i.e. *during* the first
# changelist render. ModelAdmin.changelist_view puts `actions_on_top` into the context
# before rendering starts, so that first changelist was built with Django's default and
# drew the action bar above the table; every later request got it right. Django imports
# each installed app's models module during django.setup(), long before any request, which
# makes the defaults apply deterministically.
from suit5 import config  # noqa: F401
