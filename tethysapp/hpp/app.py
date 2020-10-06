from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import PersistentStoreDatabaseSetting


class Hpp(TethysAppBase):
    """
    Tethys app class for HPP.
    """

    name = 'Hydrologic Parameter Parser'
    index = 'hpp:home'
    icon = 'hpp/images/watershedwide.jpeg'
    package = 'hpp'
    root_url = 'hpp'
    color = '#2980b9'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='hpp',
                controller='hpp.controllers.home'
            ),
            UrlMap(
                name='zone-construction',
                url='zone-construction',
                controller='hpp.controllers.zone_construction'
            ),
            UrlMap(
                name='storm-sewer-performance',
                url='storm-sewer-performance',
                controller='hpp.controllers.storm_sewer_performance'
            ),
            UrlMap(
                name='infrastructure-risk',
                url='infrastructure-risk',
                controller='hpp.controllers.infrastructure_risk'
            ),
            UrlMap(
                name='aggregated-risk',
                url='aggregated-risk',
                controller='hpp.controllers.aggregated_risk'
            ),
            UrlMap(name='zone-upload',
                url='hpp/aggregated-risk/zone-upload',
                controller='hpp.ajax_controllers.zone_upload'
            ),
            UrlMap(name='file-upload',
                url='hpp/aggregated-risk/file-upload',
                controller='hpp.ajax_controllers.file_upload'
            ),
            UrlMap(name='file-upload-move-files',
                url='hpp/aggregated-risk/file-upload-move-files',
                controller='hpp.ajax_controllers.file_upload_move_files'
            ),
            UrlMap(name='zone-spatial-join',
                url='hpp/aggregated-risk/zone-spatial-join',
                controller='hpp.ajax_controllers.zone_spatial_join'
            ),
            UrlMap(name='populate-risk-score-modal',
                url='hpp/aggregated-risk/populate-risk-score-modal',
                controller='hpp.ajax_controllers.populate_risk_score_modal'
            ),
            UrlMap(name='datatable-ajax',
                url='hpp/aggregated-risk/datatable-ajax',
                controller='hpp.ajax_controllers.datatable_ajax'
            ),
            UrlMap(name='get-mini-geojson-features',
                url='hpp/aggregated-risk/get-mini-geojson-features',
                controller='hpp.ajax_controllers.get_mini_geojson_features'
            ),

            UrlMap(name='get-zone-charts',
                url='hpp/aggregated-risk/get-zone-charts',
                controller='hpp.ajax_controllers.get_zone_charts'
            ),
            UrlMap(name='num-class-change-populate-risk-score-modal',
                   url='hpp/aggregated-risk/num-class-change-populate-risk-score-modal',
                   controller='hpp.ajax_controllers.num_class_change_populate_risk_score_modal'
            ),
            UrlMap(name='get-zone-classes-from-db',
                   url='hpp/aggregated-risk/get-zone-classes-from-db',
                   controller='hpp.ajax_controllers.get_zone_classes_from_db'
            ),
            UrlMap(name='update-max-risk-values',
                   url='hpp/aggregated-risk/update-max-risk-values',
                   controller='hpp.ajax_controllers.update_max_risk_values'
            ),
            UrlMap(name='update-min-risk-values',
                   url='hpp/aggregated-risk/update-min-risk-values',
                   controller='hpp.ajax_controllers.update_min_risk_values'
            ),
            UrlMap(name='risk-score-reclassification',
                   url='hpp/aggregated-risk/risk-score-reclassification',
                   controller='hpp.ajax_controllers.risk_score_reclassification'
            ),
            UrlMap(name='save-risk-classification-to-db',
                   url='hpp/aggregated-risk/save-risk-classification-to-db',
                   controller='hpp.ajax_controllers.save_risk_classification_to_db'
            ),
            UrlMap(name='save-weight-to-db',
                   url='hpp/aggregated-risk/save-weight-to-db',
                   controller='hpp.ajax_controllers.save_weight_to_db'
            ),
            UrlMap(name='save-zone-classification-to-db',
                   url='hpp/aggregated-risk/save-zone-classification-to-db',
                   controller='hpp.ajax_controllers.save_zone_classification_to_db'
            ),

        )

        return url_maps





    def persistent_store_settings(self):
            """
            Define Persistent Store Settings.
            """
            ps_settings = (
                PersistentStoreDatabaseSetting(
                    name='primary_db',
                    description='primary database',
                    initializer='hpp.model.init_primary_db',
                    required=True
                ),
                # PersistentStoreDatabaseSetting(
                #     name='zone_db',
                #     description='zone database',
                #     initializer='hpp.model.init_zone_db',
                #     required=True
                # ),
            )

            return ps_settings
