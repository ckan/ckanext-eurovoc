from ckan.common import _

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def eurovoc_subjects():
    '''
    Return a list of (id, label) tuples representing toplevel Eurovoc
    subjects.

    http://eurovoc.europa.eu/drupal/?q=download/subject_oriented&cl=en
    '''
    eurovoc_subjects = (
        (None, ''),
        ('politics', _('Politics')),
        ('international-relations', _('International Relations')),
        ('european-union', _('European Union')),
        ('law', _('Law')),
        ('economics', _('Economics')),
        ('trade', _('Trade')),
        ('finance', _('Finance')),
        ('social-questions', _('Social Questions')),
        ('education-and-communications', _('Education and Communications')),
        ('science', _('Science')),
        ('business-and-competition', _('Business and Competition')),
        ('employment-and-working-conditions', _('Employment and Working Conditions')),
        ('transport', _('Transport')),
        ('environment', _('Environment')),
        ('agriculture-forestry-and-fisheries', _('Agriculture, Forestry and Fisheries')),
        ('agri-foodstuffs', _('Agri-foodstuffs')),
        ('production-technology-and-research', _('Production, Technology and Research')),
        ('energy', _('Energy')),
        ('industry', _('Industry')),
        ('geography', _('Geography')),
        ('international-organisations', _('International Organisations')),
    )
    return eurovoc_subjects


def _eurovoc_text_output(id):
    '''Return the label value for a given subject id.'''
    subject_dict = dict(eurovoc_subjects())
    return subject_dict.get(id, None)


class EurovocPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IValidators)

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    # IDatasetForm

    def _modify_package_schema(self, schema):
        schema.update({
            'eurovoc_subject': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        return schema

    def create_package_schema(self):
        schema = super(EurovocPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(EurovocPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(EurovocPlugin, self).show_package_schema()
        schema.update({
            'eurovoc_subject': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('eurovoc_text_output'),
                toolkit.get_validator('ignore_missing')
            ]
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    # ITemplateHelpers

    def get_helpers(self):
        return {'eurovoc_subjects': eurovoc_subjects}

    # IValidators

    def get_validators(self):
        return {
            'eurovoc_text_output': _eurovoc_text_output,
        }
