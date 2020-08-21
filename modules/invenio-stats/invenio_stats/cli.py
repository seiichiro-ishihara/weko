# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Aggregation classes."""

from __future__ import absolute_import, print_function

from functools import wraps

import click
from dateutil.parser import parse as dateutil_parse
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.local import LocalProxy

from .proxies import current_stats
from .tasks import aggregate_events, process_events
from .utils import cli_delete_es_index, cli_restore_es_data_from_db, \
    get_aggregation_data_from_db, get_bookmark_data_from_db, \
    get_event_data_from_db, prepare_es_indexes


def abort_if_false(ctx, param, value):
    """Abort command if value is False."""
    if not value:
        ctx.abort()


def lazy_result(f):
    """Decorate function to return LazyProxy."""

    @wraps(f)
    def decorated(ctx, param, value):
        return LocalProxy(lambda: f(ctx, param, value))

    return decorated


@lazy_result
def _validate_event_type(ctx, param, value):
    invalid_values = set(value) - set(current_stats.enabled_events)
    if invalid_values:
        raise click.BadParameter(
            'Invalid event type(s): {}. Valid values: {}'.format(
                ', '.join(invalid_values),
                ', '.join(current_stats.enabled_events)))
    return value


def _verify_date(ctx, param, value):
    if value:
        dateutil_parse(value)
        return value


def _parse_date(ctx, param, value):
    if value:
        return dateutil_parse(value)


@lazy_result
def _validate_aggregation_type(ctx, param, value):
    invalid_values = set(value) - set(current_stats.enabled_aggregations)
    if invalid_values:
        raise click.BadParameter(
            'Invalid aggregation type(s): {}. Valid values: {}'.format(
                ', '.join(invalid_values),
                ', '.join(current_stats.enabled_aggregations)))
    return value


events_arg = click.argument(
    'event-types', nargs=-1, callback=_validate_event_type)

aggregation_arg = click.argument(
    'aggregation-types', nargs=-1, callback=_validate_event_type)

aggr_arg = click.argument(
    'aggregation-types', nargs=-1, callback=_validate_aggregation_type)


@click.group()
def stats():
    """Statistics commands."""


@stats.group()
def events():
    """Event management commands."""


@events.command('process')
@click.argument('event-types', nargs=-1, callback=_validate_event_type)
@click.option('--eager', '-e', is_flag=True)
@with_appcontext
def _events_process(event_types=None, eager=False):
    """Process stats events."""
    event_types = event_types or list(current_stats.enabled_events)
    if eager:
        process_events.apply((event_types,), throw=True)
        click.secho('Events processed successfully.', fg='green')
    else:
        process_events.delay(event_types)
        click.secho('Events processing task sent...', fg='yellow')


@events.command('delete')
@events_arg
@click.option(
    '--suffix', '-s',
    default='*',
    help='Suffix of index, if not entered then default is *. Ex: 2020'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    default=False,
    help='Ignore Elasticsearch errors '
         'when performing Elasticsearch index deletion.'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    default=False,
    help='Displays information about indexes to be deleted.'
)
@click.option(
    '--yes-i-know',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Do you know that you are going to delete the event(s) index?',
    help='Confirm deletion of the Elasticsearch index.'
)
@with_appcontext
def _events_delete(event_types, suffix, force, verbose):
    """Delete event index(es) on Elasticsearch.

    EVENT_TYPES: The event types.
    (event type value: celery-task|file-download|file-preview|record-view|item-create|search|top-view)
    """
    event_types = event_types or list(current_stats.enabled_events)
    suffix = suffix or "*"
    event_prefix = current_app.config['STATS_EVENT_STRING']
    for event_index in prepare_es_indexes(event_types, event_prefix, suffix):
        cli_delete_es_index(event_index, force, verbose)


@events.command('restore')
@events_arg
@click.option(
    '--suffix', '-s',
    default=None,
    help='Suffix of index, if not entered then default is None. Ex: 2020'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    default=False,
    help='Ignore Elasticsearch errors '
         'when performing Elasticsearch index restoration.'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    default=False,
    help='Displays information about indexes to be restored.'
)
@with_appcontext
def _events_restore(event_types, suffix, force, verbose):
    """Restore event index(es) on Elasticsearch based on Database.

    EVENT_TYPES: The event types.
    (event type value: celery-task|file-download|file-preview|record-view|item-create|search|top-view)
    """
    event_prefix = current_app.config['STATS_EVENT_STRING']
    event_data = get_event_data_from_db(event_types, event_prefix, suffix)
    cli_restore_es_data_from_db(event_data, force, verbose)


@stats.group()
def aggregations():
    """Aggregation management commands."""


@aggregations.command('process')
@aggr_arg
@click.option('--start-date', callback=_verify_date)
@click.option('--end-date', callback=_verify_date)
@click.option('--update-bookmark', '-b', is_flag=True)
@click.option('--eager', '-e', is_flag=True)
@with_appcontext
def _aggregations_process(aggregation_types=None,
                          start_date=None, end_date=None,
                          update_bookmark=False, eager=False):
    """Process stats aggregations."""
    aggregation_types = (aggregation_types
                         or list(current_stats.enabled_aggregations))
    if eager:
        aggregate_events.apply(
            (aggregation_types,),
            dict(start_date=start_date, end_date=end_date,
                 update_bookmark=update_bookmark),
            throw=True)
        click.secho('Aggregations processed successfully.', fg='green')
    else:
        aggregate_events.delay(
            aggregation_types, start_date=start_date, end_date=end_date)
        click.secho('Aggregations processing task sent...', fg='yellow')


@aggregations.command('delete')
@aggr_arg
@click.option('--start-date', callback=_parse_date)
@click.option('--end-date', callback=_parse_date)
@click.confirmation_option(
    prompt='Are you sure you want to delete aggregations?')
@with_appcontext
def _aggregations_delete(aggregation_types=None,
                         start_date=None, end_date=None):
    """Delete computed aggregations."""
    aggregation_types = (aggregation_types
                         or list(current_stats.enabled_aggregations))
    for a in aggregation_types:
        aggr_cfg = current_stats.aggregations[a]
        aggregator = aggr_cfg.aggregator_class(
            name=aggr_cfg.name, **aggr_cfg.aggregator_config)
        aggregator.delete(start_date, end_date)


@aggregations.command('list-bookmarks')
@aggr_arg
@click.option('--start-date', callback=_parse_date)
@click.option('--end-date', callback=_parse_date)
@click.option('--limit', '-n', default=5)
@with_appcontext
def _aggregations_list_bookmarks(aggregation_types=None,
                                 start_date=None, end_date=None, limit=None):
    """List aggregation bookmarks."""
    aggregation_types = (aggregation_types
                         or list(current_stats.enabled_aggregations))
    for a in aggregation_types:
        aggr_cfg = current_stats.aggregations[a]
        aggregator = aggr_cfg.aggregator_class(
            name=aggr_cfg.name, **aggr_cfg.aggregator_config)
        bookmarks = aggregator.list_bookmarks(start_date, end_date, limit)
        click.echo('{}:'.format(a))
        for b in bookmarks:
            click.echo(' - {}'.format(b.date))


@aggregations.command('delete-index')
@aggregation_arg
@click.option(
    '--bookmark', '-b',
    is_flag=True,
    default=False,
    help='Delete bookmark index on Elasticsearch.'
)
@click.option(
    '--suffix', '-s',
    default='*',
    help='Suffix of index, if not entered then default is *. Ex: 2020'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    default=False,
    help='Ignore Elasticsearch errors '
         'when performing Elasticsearch index deletion.'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    default=False,
    help='Displays information about indexes to be deleted.'
)
@click.option(
    '--yes-i-know',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Do you know that you are going to delete the aggregation(s) index?',
    help='Confirm deletion of the Elasticsearch index.'
)
@with_appcontext
def _aggregations_delete_index(
    aggregation_types=None,
    bookmark=False, suffix=None,
    force=False, verbose=False
):
    """Delete aggregation index (and bookmark index) on Elasticsearch.

    AGGREGATION_TYPES: The aggregation types.
    (Aggregation type value: celery-task|file-download|file-preview|record-view|item-create|search|top-view)
    """
    aggregation_types = (aggregation_types
                         or current_app.config['STATS_AGGREGATION_INDEXES'])
    suffix = suffix or "*"
    for aggregation_index in prepare_es_indexes(aggregation_types, None,
                                                suffix):
        cli_delete_es_index(aggregation_index, force, verbose)
    if bookmark:
        for bookmark_index in prepare_es_indexes(aggregation_types, None,
                                                 suffix, bookmark):
            cli_delete_es_index(bookmark_index, force, verbose)


@aggregations.command('restore')
@aggregation_arg
@click.option(
    '--bookmark', '-b',
    is_flag=True,
    default=False,
    help='Delete bookmark index on Elasticsearch.'
)
@click.option(
    '--suffix', '-s',
    default=None,
    help='Suffix of index, if not entered then default is None. Ex: 2020'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    default=False,
    help='Ignore Elasticsearch errors '
         'when performing Elasticsearch index restoration.'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    default=False,
    help='Displays information about indexes to be restored.'
)
@with_appcontext
def _aggregations_restore(
    aggregation_types=None,
    bookmark=False, suffix=None,
    force=False, verbose=False
):
    """Restore aggregation index (and bookmark index) on Elasticsearch.

    AGGREGATION_TYPES: The aggregation types.
    (Aggregation type value: celery-task|file-download|file-preview|record-view|item-create|search|top-view)
    """
    aggregation_types = (aggregation_types
                         or current_app.config['STATS_AGGREGATION_INDEXES'])
    click.secho(
        'Starting migration of Aggregation data '
        'from the Database to Elasticsearch...',
        fg='green'
    )
    flush_indices = set()
    aggregation_data = get_aggregation_data_from_db(aggregation_types, suffix,
                                                    flush_indices)
    cli_restore_es_data_from_db(aggregation_data, force, verbose)
    if bookmark:
        click.secho(
            'Starting migration of Bookmark data '
            'from the Database to Elasticsearch...',
            fg='green'
        )
        bookmark_data = get_bookmark_data_from_db(aggregation_types, suffix,
                                                  bookmark)
        cli_restore_es_data_from_db(bookmark_data, force, verbose)
