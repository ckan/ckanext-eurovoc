import os.path
import json

from ckan.common import _
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class EurovocPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):

    '''Add top-level Eurovoc categories to the dataset schema.'''

    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IFacets)

    def __init__(self, *args, **kwargs):
        self.categories = []

    # IConfigurable

    def configure(self, config):
        '''
        Get and parse a categories config file to determine the correct label
        language and additional search terms for each eurovoc category.
        '''
        categories_config_filename = config.get('ckanext.eurovoc.categories',
                                                None)
        # If no filename is defined in the config, default to en.
        if categories_config_filename is None:
            categories_config_filename = 'categories_en.json'

        categories_json = os.path.join(os.path.dirname(__file__),
                                       'categories',
                                       categories_config_filename)

        with open(categories_json) as categories_list:
            self.categories = json.load(categories_list)

    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

    # IDatasetForm

    def _modify_package_schema(self, schema):
        schema.update({
            'eurovoc_category': [
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
            'eurovoc_category': [
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
        return {'eurovoc_categories': self._eurovoc_categories_helper}

    # IValidators

    def get_validators(self):
        return {
            'eurovoc_text_output': self._eurovoc_text_output,
        }

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        self._update_facets(facets_dict)
        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        self._update_facets(facets_dict)
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        self._update_facets(facets_dict)
        return facets_dict

    def _update_facets(self, facets_dict):
        facets_dict.update({
            'eurovoc_category_label': plugins.toolkit._('Eurovoc Categories')
        })

    # IPackageController

    def before_index(self, dataset_dict):
        '''
        Insert `eurovoc_category_label` and `vocab_eurovoc_category_terms`
        into solr index derived from the dataset_dict's `eurovoc_category`
        field.
        '''
        eurovoc_category = dataset_dict.get('eurovoc_category', None)
        if eurovoc_category is not None:
            label = self._eurovoc_text_output(eurovoc_category)
            search_terms = []
            if label is not None:
                search_terms.append(label)
                dataset_dict['eurovoc_category_label'] = label

            additional_search_terms = self._eurovoc_additional_search_terms(eurovoc_category)
            if additional_search_terms is not None:
                search_terms.extend(additional_search_terms)
                dataset_dict['vocab_eurovoc_category_terms'] = search_terms

        return dataset_dict

    # Private methods

    def _eurovoc_categories_helper(self):
        '''
        Return a list of (id, label) tuples representing toplevel Eurovoc
        categories.
        '''
        eurovoc_categories = [(cat['id'], cat['label']) for cat in
                              self.categories]
        eurovoc_categories.insert(0, ('', _('No category')))
        return eurovoc_categories

    def _get_value_for_key_in_category(self, id, key):
        '''
        Return a value from a category dict in self.categories where the
        category id corresponding with the passed `id`, and the value
        corresponds with the passed key.
        '''
        category = next((cat for cat in self.categories if cat['id'] == id),
                        None)

        if category:
            return category[key]
        else:
            return None

    def _eurovoc_text_output(self, id):
        '''Return the label value for a given category id.'''
        return self._get_value_for_key_in_category(id, 'label')

    def _eurovoc_additional_search_terms(self, id):
        '''
        Return a list of additional search terms for a given category
        id.
        '''
        return self._get_value_for_key_in_category(id, 'additional_search_terms')
