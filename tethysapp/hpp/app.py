from tethys_sdk.base import TethysAppBase, url_map_maker


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

        )

        return url_maps