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

"""Utilities for convert XML."""

import itertools
import re
from functools import reduce

from flask import current_app, request
from invenio_oaiserver.response import NS_OAIPMH, NS_OAIPMH_XSD, NS_XSI, \
    NSMAP, header, verb
from invenio_records_ui.utils import obj_or_import_string
from lxml import etree
from lxml.etree import Element, ElementTree, SubElement
from weko_deposit.api import WekoRecord

from .schema import SchemaTree

MISSING = object()


def dumps_oai_etree(pid, records, **kwargs):
    """Dump records into a etree.

    :param pid: The :class:`invenio_pidstore.models.PersistentIdentifier`
        instance.
    :param records: The :class:`invenio_records.api.Record` instance.
    :param schema_type: schema type
    :returns: A LXML Element instance.

    """
    serializer = obj_or_import_string(
        "weko_schema_ui.serializers.WekoCommonSchema")
    return serializer.serialize_oaipmh(pid, records, kwargs.get("schema_type"))


def dumps_etree(records, schema_type):
    """Dump records into a etree.

    :param records: The :class:`invenio_records.api.Record` instance.
    :param schema_type: schema type
    :returns: A LXML Element instance.

    """
    if schema_type:
        if records.get('metadata', {}).get('_item_metadata'):
            records['metadata'] = records['metadata'].get('_item_metadata', {})
        scname = schema_type if re.search(
            r'.*_mapping', schema_type) else schema_type + "_mapping"
        stree = SchemaTree(records, scname)
        return stree.create_xml()


def get_identifier(record):
    """Get Identifier of record(DOI or HDL), if not set URL as default.

    @param record:
    @return:
    """
    result = {
        "attribute_name": "Identifier",
        "attribute_value_mlt": [
            {
                "subitem_systemidt_identifier": "",
                "subitem_systemidt_identifier_type": ""
            }
        ]
    }
    record_deposit = record.get('metadata').get('_deposit')
    if record_deposit:
        record_id = record_deposit.get('id')
        record = WekoRecord.get_record_by_pid(record_id)
        if record.pid_doi:
            identifier = record.pid_doi.pid_value
            identifier_type = record.pid_doi.pid_type.upper()
        elif record.pid_cnri:
            identifier = record.pid_cnri.pid_value
            identifier_type = record.pid_cnri.pid_type.upper()
        else:
            identifier = current_app.config['WEKO_SCHEMA_RECORD_URL'].format(
                request.url_root, record_id)
            identifier_type = 'URI'
        result['attribute_value_mlt'][0][
            'subitem_systemidt_identifier'] = identifier
        result['attribute_value_mlt'][0][
            'subitem_systemidt_identifier_type'] = identifier_type
    else:
        result = {}
    return result


def dumps(records, schema_type=None, **kwargs):
    """
    Dumps.

    :param records:
    :param schema_type:
    :param kwargs:
    :return: xml string

    """
    if records["metadata"].get("@export_schema_type"):
        est = records["metadata"].pop("@export_schema_type")

    oid = records["metadata"].get('_oai').get('id')
    root = export_tree(
        record=records,
        metadataPrefix=est,
        identifier=oid,
        verb='GetRecord')
    # root = dumps_etree(records=records, schema_type=est)
    return etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding='UTF-8',
        **kwargs
    )


def export_tree(record, **kwargs):
    """Create OAI-PMH response for verb Identify."""
    e_tree, e_getrecord = verb(**kwargs)
    e_record = SubElement(e_getrecord, etree.QName(NS_OAIPMH, 'record'))

    import dateutil.parser
    header(
        e_record,
        identifier=record.get('control_number'),
        datestamp=dateutil.parser.parse(record.get('updated')),
        sets=record.get('_oai', {}).get('sets', []),
    )
    e_metadata = SubElement(e_record,
                            etree.QName(NS_OAIPMH, 'metadata'))
    e_metadata.append(
        dumps_etree(
            records=record,
            schema_type=kwargs['metadataPrefix']))

    root = e_tree.getroot()
    e_oaipmh = Element(etree.QName(NS_OAIPMH, 'OAI-PMH'), nsmap=NSMAP)
    e_oaipmh.set(etree.QName(NS_XSI, 'schemaLocation'),
                 '{0} {1}'.format(NS_OAIPMH, NS_OAIPMH_XSD))
    e_tree = ElementTree(element=e_oaipmh)
    for e in root.getchildren():
        e_oaipmh.append(e)
    root.clear()

    return e_tree


def json_merge_all(json_lst):
    """Json_merge_all."""
    merged = reduce(json_merge, json_lst, MISSING)
    if merged == MISSING:
        raise ValueError("json_lst was empty")
    return merged


def json_merge(a, b):
    """Json_merge."""
    if isinstance(a, dict) and isinstance(b, dict):
        return dict(
            (k, json_merge(a_val, b_val))
            for k, a_val, b_val in dict_zip(a, b, fillvalue=MISSING)
        )
    elif isinstance(a, list) and isinstance(b, list):
        return list(itertools.chain(a, b))

    if b is MISSING:
        assert a is not MISSING
        return a
    return b


def dict_zip(*dicts, **kwargs):
    """Dict_zip."""
    fillvalue = kwargs.get("fillvalue", None)
    keys = reduce(set.union, [set(d.keys()) for d in dicts], set())
    return [tuple([k] + [d.get(k, fillvalue) for d in dicts]) for k in keys]
