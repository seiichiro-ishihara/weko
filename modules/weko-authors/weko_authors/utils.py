# -*- coding: utf-8 -*-
#
# This file is part of WEKO3.
# Copyright (C) 2017 National Institute of Informatics.
#
# WEKO3 is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# WEKO3 is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WEKO3; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.

"""Utils for weko-authors."""

import base64
import csv
import io
import sys
import tempfile
import traceback
from copy import deepcopy
from functools import reduce
from operator import getitem
from sys import stdout

from flask import current_app
from flask_babelex import gettext as _
from invenio_cache import current_cache
from invenio_db import db
from invenio_files_rest.models import FileInstance, Location
from invenio_indexer.api import RecordIndexer

from weko_authors.contrib.validation import validate_by_extend_validator, \
    validate_external_author_identifier, validate_map, validate_required

from .api import WekoAuthors
from .config import WEKO_AUTHORS_EXPORT_CACHE_STATUS_KEY, \
    WEKO_AUTHORS_EXPORT_CACHE_URL_KEY, WEKO_AUTHORS_TSV_MAPPING
from .models import AuthorsPrefixSettings


def get_author_setting_obj(scheme):
    """Check item Scheme exist in DB."""
    try:
        return db.session.query(AuthorsPrefixSettings).filter(
            AuthorsPrefixSettings.scheme == scheme).one_or_none()
    except Exception as ex:
        current_app.logger.debug(ex)
    return None


def check_email_existed(email: str):
    """Check email has existed.

    :param email: email string.
    :returns: author info.
    """
    body = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"gather_flg": 0}},
                    {"term": {"emailInfo.email.raw": email}}
                ]
            }
        }
    }

    indexer = RecordIndexer()
    result = indexer.client.search(
        index=current_app.config['WEKO_AUTHORS_ES_INDEX_NAME'],
        doc_type=current_app.config['WEKO_AUTHORS_ES_DOC_TYPE'],
        body=body
    )

    if result['hits']['total']:
        return {
            'email': email,
            'author_id': result['hits']['hits'][0]['_source']['pk_id']
        }
    else:
        return {
            'email': email,
            'author_id': ''
        }


def get_export_status():
    """Get export status from cache."""
    return current_cache.get(WEKO_AUTHORS_EXPORT_CACHE_STATUS_KEY) or {}


def set_export_status(start_time=None, task_id=None):
    """Set export status into cache."""
    data = get_export_status() or dict()
    if start_time:
        data['start_time'] = start_time
    if task_id:
        data['task_id'] = task_id

    current_cache.set(WEKO_AUTHORS_EXPORT_CACHE_STATUS_KEY, data, timeout=0)
    return data


def delete_export_status():
    """Delete export status."""
    current_cache.delete(WEKO_AUTHORS_EXPORT_CACHE_STATUS_KEY)


def get_export_url():
    """Get exported info from cache."""
    return current_cache.get(WEKO_AUTHORS_EXPORT_CACHE_URL_KEY) or {}


def save_export_url(start_time, end_time, file_uri):
    """Save exported info into cache."""
    data = dict(
        start_time=start_time,
        end_time=end_time,
        file_uri=file_uri
    )

    current_cache.set(WEKO_AUTHORS_EXPORT_CACHE_URL_KEY, data, timeout=0)
    return data


def export_authors():
    """Export all authors."""
    file_uri = None
    try:
        mappings = deepcopy(WEKO_AUTHORS_TSV_MAPPING)
        authors = WekoAuthors.get_all(with_deleted=False, with_gather=False)
        schemes = WekoAuthors.get_identifier_scheme_info()
        row_header, row_label_en, row_label_jp, row_data = \
            WekoAuthors.prepare_export_data(mappings, authors, schemes)

        # write csv data to a stream
        csv_io = io.StringIO()
        writer = csv.writer(csv_io, delimiter='\t',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows([row_header, row_label_en, row_label_jp, *row_data])
        reader = io.BufferedReader(io.BytesIO(
            csv_io.getvalue().encode("utf-8")))

        # save data into location
        cache_url = get_export_url()
        if not cache_url:
            file = FileInstance.create()
            file.set_contents(
                reader, default_location=Location.get_default().uri)
        else:
            file = FileInstance.get_by_uri(cache_url['file_uri'])
            file.writable = True
            file.set_contents(reader)

        file_uri = file.uri if file else None
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        current_app.logger.error(ex)
        traceback.print_exc(file=stdout)

    return file_uri


def check_import_data(file_name: str, file_content: str):
    """Validation importing tsv file.

    :argument
        file_name -- file name.
        file_content -- content file's name.
    :return
        return       -- check information.
    """
    tmp_prefix = current_app.config['WEKO_AUTHORS_IMPORT_TMP_PREFIX']
    temp_file = tempfile.NamedTemporaryFile(prefix=tmp_prefix)
    result = {}

    try:
        temp_file.write(base64.b64decode(file_content))
        temp_file.flush()

        flat_mapping_all, flat_mapping_ids = flatten_authors_mapping(
            WEKO_AUTHORS_TSV_MAPPING)
        tsv_data = unpackage_and_check_import_file(
            file_name, temp_file.name, flat_mapping_ids)
        result['list_import_data'] = validate_import_data(
            tsv_data, flat_mapping_ids, flat_mapping_all)
    except Exception as ex:
        error = _('Internal server error')
        if isinstance(ex, UnicodeDecodeError):
            error = ex.reason
        elif ex.args and len(ex.args) and isinstance(ex.args[0], dict) \
                and ex.args[0].get('error_msg'):
            error = ex.args[0].get('error_msg')
        result['error'] = error
        current_app.logger.error('-' * 60)
        traceback.print_exc(file=sys.stdout)
        current_app.logger.error('-' * 60)

    return result


def unpackage_and_check_import_file(tsv_file_name, temp_file, mapping_ids):
    """Unpackage and check format of import file.

    Args:
        tsv_file_name (str): File uploaded name.
        temp_file (str): Temp file path.
        mapping_ids (list): List only mapping ids.

    Returns:
        list: Tsv data.
    """
    from weko_search_ui.utils import handle_check_consistence_with_mapping, \
        handle_check_duplication_item_id, parse_to_json_form
    header = []
    tsv_data = []
    with open(temp_file, 'r') as file:
        csv_reader = csv.reader(file, delimiter='\t')
        try:
            for num, data_row in enumerate(csv_reader, start=1):
                if num == 1:
                    header = data_row
                    header[0] = header[0].replace('#', '', 1)
                    duplication_item_ids = \
                        handle_check_duplication_item_id(header)
                    if duplication_item_ids:
                        msg = _(
                            'The following metadata keys are duplicated.'
                            '<br/>{}')
                        raise Exception({
                            'error_msg':
                                msg.format('<br/>'.join(duplication_item_ids))
                        })

                    not_consistent_list = \
                        handle_check_consistence_with_mapping(mapping_ids,
                                                              header)
                    if not_consistent_list:
                        msg = _('The item does not consistent with the '
                                'specified database.<br/>{}')
                        raise Exception({
                            'error_msg': msg.format(
                                '<br/>'.join(not_consistent_list))
                        })
                elif num in [2, 3] and data_row[0].startswith('#'):
                    continue
                elif num > 3:
                    data_parse_metadata = parse_to_json_form(
                        zip(header, data_row),
                        include_empty=True
                    )

                    if not data_parse_metadata:
                        raise Exception({
                            'error_msg': _('Cannot read tsv file correctly.')
                        })

                    tsv_data.append(dict(**data_parse_metadata))

            if not tsv_data:
                raise Exception({
                    'error_msg': _('There is no data to import.')
                })
        except UnicodeDecodeError as ex:
            ex.reason = _('The TSV file could not be read. Make sure the file'
                          + ' format is TSV and that the file is'
                          + ' UTF-8 encoded.').format(tsv_file_name)
            raise ex
        except Exception as ex:
            raise ex

    return tsv_data


def validate_import_data(tsv_data, mapping_ids, mapping):
    """Validate import data.

    Args:
        tsv_data (list): Author data from tsv.
        mapping_ids (list): List only mapping ids.
        mapping (list): List mapping.
    """
    authors_prefix = {}
    with db.session.no_autoflush:
        authors_prefix = AuthorsPrefixSettings.query.all()
        authors_prefix = {
            prefix.scheme: prefix.id for prefix in authors_prefix}

    list_import_id = []
    existed_authors_id, existed_external_authors_id = \
        WekoAuthors.get_author_for_validation()

    for item in tsv_data:
        errors = []
        warnings = []

        weko_id = item.get('pk_id')
        # check duplication WEKO ID
        if weko_id and weko_id not in list_import_id:
            list_import_id.append(weko_id)
        elif weko_id:
            warnings.append(_('There is duplicate data in the TSV file.'))

        # set status
        set_record_status(existed_authors_id, item, errors)

        # get data folow by mapping
        data_by_mapping = {}
        for _key in mapping_ids:
            data_by_mapping[_key] = get_values_by_mapping(
                _key.split('.'), item)

        # Validation
        for field in mapping:
            _key = field['key']
            values = data_by_mapping[_key]
            validation = field['validation']

            # check required
            if validation.get('required'):
                errors_key = validate_required(
                    item, values, validation.get('required'))
                if errors_key:
                    errors.extend(list(map(
                        lambda k: _('{} is required item.').format(k),
                        errors_key
                    )))

            # check allow data
            if validation.get('map'):
                errors_key = validate_map(
                    values, validation.get('map'))
                if errors_key:
                    error_msg = _('{} should be set by one of {}.')
                    errors.extend(list(map(
                        lambda k: error_msg.format(k, validation.get('map')),
                        errors_key
                    )))

            # check by extend validator
            if validation.get('validator'):
                errors_msg = validate_by_extend_validator(
                    values, validation.get('validator'))
                if errors_msg:
                    errors.extend(errors_msg)

            # autofill data if empty
            if not errors and field.get('autofill'):
                autofill_data(item, values, field.get('autofill'))

            # convert mask data
            if not errors and field.get('mask'):
                convert_data_by_mask(item, values, field.get('mask'))

            if _key == 'authorIdInfo[0].idType':
                # convert scheme data
                convert_scheme_to_id(item, values, authors_prefix)
                # check external author identifier exist
                warning = validate_external_author_identifier(
                    item, values, existed_external_authors_id)
                if warning:
                    warnings.append(warning)

        if errors:
            item['errors'] = item['errors'] + errors \
                if item.get('errors') else errors
            item['errors'] = list(set(item['errors']))
        if warnings:
            item['warnings'] = item['warnings'] + warnings \
                if item.get('warnings') else warnings
            item['warnings'] = list(set(item['warnings']))

    return tsv_data


def get_values_by_mapping(keys, data, parent_key=None):
    """Get values folow by mapping."""
    result = []
    current_key = keys[0].replace('[0]', '')
    current_key_with_parent = parent_key + '.' + \
        current_key if parent_key else current_key
    current_data = data.get(current_key)

    if isinstance(current_data, list):
        for idx, item in enumerate(current_data):
            result.extend(get_values_by_mapping(
                keys[1:],
                item,
                current_key_with_parent + '[{}]'.format(idx)
            ))
    elif isinstance(current_data, dict):
        result.extend(get_values_by_mapping(
            keys[1:], current_data, current_key_with_parent))
    else:
        reduce_keys = [
            (int(k.replace(']', '')) if k.endswith(']') else k)
            for k in current_key_with_parent.replace('[', '.').split('.')
        ]
        result = [{
            'key': current_key_with_parent,
            'reduce_keys': reduce_keys,
            'value': current_data
        }]
    return result


def autofill_data(item, values, autofill_data):
    """Autofill data if empty."""
    for value in values:
        if not value['value']:
            reduce_keys = value['reduce_keys']
            uplevel_data = reduce(getitem, reduce_keys[:-1], item)

            # check either required
            either_required = autofill_data.get('condition', {}) \
                .get('either_required', [])
            if either_required:
                check = [cond for cond in either_required
                         if uplevel_data.get(cond)]
                autofill_val = ''
                if check:
                    autofill_val = autofill_data.get('value', '')
                uplevel_data[reduce_keys[-1]] = autofill_val


def convert_data_by_mask(item, values, mask):
    """Convert data if have mask."""
    for value in values:
        if value['value']:
            import_value = [key for key, val in mask.items()
                            if val == value['value']]
            import_value = import_value[0] == 'true' if import_value else False
            reduce_keys = value['reduce_keys']
            reduce(getitem, reduce_keys[:-1],
                   item)[reduce_keys[-1]] = import_value


def convert_scheme_to_id(item, values, authors_prefix):
    """Convert scheme to id."""
    for value in values:
        if value['value']:
            reduce_keys = value['reduce_keys']
            reduce(getitem, reduce_keys[:-1], item)[reduce_keys[-1]] = \
                authors_prefix.get(value['value'], None)


def set_record_status(list_existed_author_id, item, errors):
    """Set status to import data."""
    item['status'] = 'new'
    pk_id = item.get('pk_id')
    err_msg = _("Specified WEKO ID does not exist.")

    if item.get('is_deleted', '') == 'D':
        item['status'] = 'deleted'
        if not pk_id or int(pk_id) not in list_existed_author_id:
            errors.append(err_msg)
    elif pk_id:
        if int(pk_id) in list_existed_author_id:
            item['status'] = 'update'
        else:
            errors.append(err_msg)


def flatten_authors_mapping(mapping, parent_key=None):
    """Flatten author mappings."""
    result_all = []
    result_keys = []
    for item in mapping:
        current_key = parent_key + '[0].' + item['json_id'] \
            if parent_key else item['json_id']
        if item.get('child'):
            child_result_all, child_result_keys = flatten_authors_mapping(
                item['child'], current_key)
            if child_result_all and child_result_keys:
                result_all.extend(child_result_all)
                result_keys.extend(child_result_keys)
        else:
            result_all.append(dict(
                key=current_key,
                label=dict(
                    en=item['label_en'],
                    jp=item['label_jp']
                ),
                mask=item.get('mask', {}),
                validation=item.get('validation', {}),
                autofill=item.get('autofill', '')
            ))
            result_keys.append(current_key)
    return result_all, result_keys


def import_author_to_system(author):
    """Import author to DB and ES.

    Args:
        author (object): Author metadata from tsv.
    """
    if author:
        try:
            status = author['status']
            del author['status']

            author["is_deleted"] = True if author.get("is_deleted") else False
            if not author.get('authorIdInfo'):
                author["authorIdInfo"] = []
            if status == 'new':
                WekoAuthors.create(author)
            else:
                author["authorIdInfo"].insert(
                    0,
                    {
                        "idType": "1",
                        "authorId": author['pk_id'],
                        "authorIdShowFlg": "true"
                    }
                )
                WekoAuthors.update(author['pk_id'], author)
            db.session.commit()
        except Exception:
            db.session.rollback()
            current_app.logger.error(
                'Author id: %s import error.' % author['pk_id'])
            traceback.print_exc(file=sys.stdout)
            raise
