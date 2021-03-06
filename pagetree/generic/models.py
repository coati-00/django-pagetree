from django import forms
from django.db import models
try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    # Old location for django 1.6
    from django.contrib.contenttypes.generic import GenericRelation

from pagetree.models import Hierarchy, UserPageVisit, PageBlock


class BasePageBlock(models.Model):
    """An abstract pageblock to be used for custom pageblocks."""

    class Meta:
        abstract = True

    display_name = 'Unimplemented BasePageBlock'
    pageblocks = GenericRelation(PageBlock)

    def needs_submit(self):
        """Determines whether this pageblock needs form controls rendered.

        If needs_submit is True, then pagetree will create a <form>
        on this pageblock's surrounding page, and a Submit button for
        that form. It may also render a "Clear results" button, under
        the right circumstances. The surrounding <form> allows pagetree
        to handle form submissions for multiple blocks on the same page.

        Also, when needs_submit is True, the POST data on the Section's
        submit() step gets processed, but when needs_submit is False,
        nothing is sent to the server.

        :returns: a boolean
        """

        return False

    def unlocked(self, user):
        """Determines whether the user can proceed past this block.

        The current user is passed in to this function, allowing you to,
        for example, find out if that user has submitted the info
        necessary to proceed past this block's page.

        :param user: the current user
        :returns: a boolean
        """

        return True

    def submit(self, user, request_data):
        """Handle this pageblock's form submission.

        :returns: None
        """

        pass

    def redirect_to_self_on_submit(self):
        """Determines where the user is redirected to on page submission.

        If submit returns True, then the user will be redirected to the
        next page in the hierarchy. Otherwise, they be redirected to the
        current page.

        :returns: a boolean
        """

        return True

    def clear_user_submissions(self, user):
        """A hook to clear any user submissions for this block.

        :returns: None
        """

        pass

    def pageblock(self):
        return self.pageblocks.first()

    # TODO: I'd like to have all the following methods be inherited
    # somehow. For now these need to be copy and pasted for each custom
    # pageblock.
    @staticmethod
    def add_form():
        return BasePageBlockForm()

    def edit_form(self):
        return BasePageBlockForm(instance=self)

    @staticmethod
    def create(request):
        form = BasePageBlockForm(request.POST)
        return form.save()

    @classmethod
    def create_from_dict(cls, d):
        return cls.objects.create(**d)

    def edit(self, vals, files):
        form = BasePageBlockForm(data=vals, files=files, instance=self)
        if form.is_valid():
            form.save()


class BasePageBlockForm(forms.ModelForm):
    """Example ModelForm for the BasePageBlock.

    This is just an example. It should always be replaced with your
    own ModelForm pointing to the custom pageblock.
    """

    class Meta:
        model = BasePageBlock
