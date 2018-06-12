from tenable.tenable_io.base import TIOEndpoint

class WorkbenchesAPI(TIOEndpoint):
    def _workbench_query(filters, kw, filterdefs):
        '''
        '''
        # Initiate the query dictionary with the filters parser.
        query = self._parse_filters(filters, filterdefs)

        if 'age' in kw:
            # The age parameter is converted into the "date_range" parameter
            # for the endpoint.  The name was simply changed to be more
            # understandable.
            query['date_range'] = self._check('age', kw['age'], int)

        if 'filter_type' in kw:
            # The scans & workbenches endpoints use a serialized JSON format for
            # query parameters, hence the x.y notation.
            query['filter.search_type'] = self._check(
                'filter_type', kw['filter_type'], str, choices=['and', 'or'])

        # Return the query to the caller
        return query


    def assets(self, *filters, **kw):
        '''
        `workbenches: assets <https://cloud.tenable.com/api#/resources/workbenches/assets>`_

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('host.hostname', 'match', 'asset.com')`.  
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.
            all_fields (bool, optional):
                Should all of the available fields be returned for each returned
                asset, or just the default fields represented in the UI.  The
                default is set to `True` which will return the same level of
                detail as the workbenches: asset-info endpoint.

        Returns:
            list: List of asset resource records.
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw, 
            self._api.filters.workbench_asset_filters())

        # If all_fields is set to true or is unspecified, then we will set the
        # all_fields parameter to "full".
        if 'all_fields' in kw:
            if self._check('all_fields', kw['all_fields'], bool):
                query['all_fields'] = 'full'
        else:
            query['all_fields'] = 'full'

        return self._api.get('workbenches/assets', params=query).json()['assets']

    def asset_info(self, id, all_fields=True):
        '''
        `workbenches: asset-info <https://cloud.tenable.com/api#/resources/workbenches/asset-info>`_

        Args:
            id (str): The unique identifier (UUID) of the asset.
            all_fields (bool, optional):
                If all_fields is set to true (the default state), then an
                expanded dataset is returned as defined by the API
                documentation (linked above).

        Returns:
            dict: The resource record for the asset.
        '''
        query = {'all_fields': 'full'}

        if not self._check('all_fields', all_fields, bool):
            # if the caller chooses to get a reduced list of attributes for the
            # response, then we simply want to remove the key from from the
            # query dictionary.  The documentation states that the existance of
            # the parameter is what triggers the expanded dataset, which we
            # are returning by default.
            del(query['all_fields'])

        return self._api.get('workbenches/assets/{}/info'.format(
            self._check('id', id, 'uuid')), params=query).json()['info']

    def asset_vulns(self, id, *filters, **kw):
        '''
        `workbenches: asset-vulnerabilities <https://cloud.tenable.com/api#/resources/workbenches/asset-vulnerabilities>`_

        Args:
            id (str):
                The unique identifier of the asset to query.
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('host.hostname', 'match', 'asset.com')`.  
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            list: List of vulnerability resource records.
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/{}/vulnerabilities'.format(
                self._check('id', id, 'uuid')), params=query).json()['vulnerabilities']

    def asset_vuln_info(self, uuid, plugin_id, *filters, **kw):
        '''
        `workbenches: asset-vulnerability-info <https://cloud.tenable.com/api#/resources/workbenches/asset-vulnerability-info>`_

        Args:
            uuid (str):
                The unique identifier of the asset to query.
            plugin_id (int):
                The unique identifier of the plugin.
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('host.hostname', 'match', 'asset.com')`.  
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            list: List of vulnerability resource records.
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/{}/vulnerabilities/{}/info'.format(
                self._check('uuid', id, 'uuid'),
                self._check('plugin_id', plugin_id, int)), params=query).json()['vulnerabilities']

    def asset_vuln_output(self, uuid, plugin_id, *filters, **kw):
        '''
        `workbenches: asset-vulnerability-output <https://cloud.tenable.com/api#/resources/workbenches/asset-vulnerability-output>`_

        Args:
            uuid (str):
                The unique identifier of the asset to query.
            plugin_id (int):
                The unique identifier of the plugin.
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('host.hostname', 'match', 'asset.com')`.  
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            list: List of vulnerability resource records.
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_vuln_filters())

        return self._api.get(
            'workbenches/assets/{}/vulnerabilities/{}/outputs'.format(
                self._check('uuid', id, 'uuid'),
                self._check('plugin_id', plugin_id, int)), params=query).json()['vulnerabilities']

    def assets_with_vulns(self, *filters, **kw):
        '''
        `workbenches: assets-vulnerabilities <https://cloud.tenable.com/api#/resources/workbenches/assets-vulnerabilities>`_

        Args:
            age (int, optional):
                The maximum age of the data to be returned.
            *filters (list, optional):
                 A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('host.hostname', 'match', 'asset.com')`.  
                For a complete list of the available filters and options, please
                refer to the API documentation linked above.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.

        Returns:
            list: List of asset resource records.
        '''
        # Call the query builder to handle construction
        query = self._workbench_query(filters, kw,
            self._api.filters.workbench_asset_filters())

        return self._api.get(
            'workbenches/assets/vulnerabilities', params=query).json()['assets']

def export(self, *filters, **kw):
        '''
        `workbenches: export <https://cloud.tenable.com/api#/resources/workbenches/export-request>`_

        Args:
            *filters (tuple, optional):
                A list of tuples detailing the filters that wish to be applied
                the response data.  Each tuple is constructed as 
                ('filter', 'operator', 'value') and would look like the 
                following example: `('plugin.id', 'eq', '19506')`.  For a
                complete list of the available filters and options, please
                refer to the API documentation linked above.
            asset_uuid (uuid, optional):
                Restrict the output to the asset identifier specified.
            plugin_id (int, optional): 
                Restrict the output to the plugin identifier specified.
            format (str, optional):
                What format would you like the resulting data to be in.  The
                default would be nessus output.  Available options are `nessus`,
                `csv`, `html`, `pdf`.
            chapters (list, optional):
                A list of the chapters to write for the report.  The chapters
                list is only required for PDF and HTML exports.  Available
                chapters are `vuln_hosts_summary`, `vuln_by_host`, 
                `compliance_exec`, `remediations`, `vuln_by_plugin`, and
                `compliance`.  List order will denote output order.
            filter_type (str, optional):
                Are the filters exclusive (this AND this AND this) or inclusive
                (this OR this OR this).  Valid values are `and` and `or`.  The
                default setting is `and`.
            fobj (FileObject, optional):
                The file-like object to be returned with the exported data.  If
                no object is specified, a BytesIO object is returned with the
                data.  While this is an optional parameter, it is highly
                recommended to use this paramater as exported files can be quite
                large, and BytesIO objects are stored in memory, not on disk.

        Returns:
            FileObject: The file-like object of the requested export.
        '''

        # initiate the payload and parameters dictionaries.
        params = self._parse_filters(filters,
            self._api.filters.workbench_vuln_filters(), rtype='json')
        #params = dict()

        if 'plugin_id' in kw:
            params['plugin_id'] = self._check(
                'plugin_id', kw['plugin_id'], int)

        if 'asset_uuid' in kw:
            params['asset_id'] = self._check(
                'asset_uuid', kw['asset_uuid'], 'uuid')   

        if 'chapters' in kw:
            # The chapters are sent to us in a list, and we need to collapse
            # that down to a comma-delimited string.
            params['chapter'] = ';'.join(
                self._check('chapters', kw['chapters'], list, choices=[
                    'vuln_hosts_summary', 'vuln_by_host', 'vuln_by_plugin',
                    'compliance_exec', 'compliance', 'remediations'
                ]))

        if 'filter_type' in kw:
            params['filter.search_type'] = self._check(
                    'filter_type', kw['filter_type'], str)

        # Now we need to set the FileObject.  If one was passed to us, then lets
        # just use that, otherwise we will need to instantiate a BytesIO object
        # to push the data into.
        if 'fobj' in kw:
            fobj = kw['fobj']
        else:
            fobj = BytesIO()

        # The first thing that we need to do is make the request and get the
        # File id for the job.
        fid = self._api.post('workbenches/export', 
            params=params).json()['file']

        # Next we will wait for the statif of the export request to become
        # ready.  We will query the API every half a second until we get the
        # response we're looking for.
        while 'ready' != self._api.get('workbenches/export/{}/status'.format(
                fid)).json()['status']:
            time.sleep(0.5)

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._api.get('workbenches/export/{}/download'.format(
            fid), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)


