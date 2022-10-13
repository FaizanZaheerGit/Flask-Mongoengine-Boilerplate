# Python imports
import uuid
import mongoengine

# Local imports
from FlaskMongoengineBoilerplate.utils import constants, common_utils


def read_single_record(collection, read_filter):
    """
    read and return single record
    :param collection:
    :param read_filter:
    :return:
    """
    if type(read_filter) == mongoengine.queryset.visitor.Q or \
            type(read_filter) == mongoengine.queryset.visitor.QCombination:
        return collection.objects(read_filter).order_by("-"+constants.CREATED_AT).first()

    return collection.objects(**read_filter).order_by("-"+constants.CREATED_AT).first()


def read_record(collection, read_filter):
    """
    read and return multiple records based on the read filter
    :param collection:
    :param read_filter:
    :return:
    """
    if type(read_filter) == mongoengine.queryset.visitor.Q or \
            type(read_filter) == mongoengine.queryset.visitor.QCombination:
        return collection.objects(read_filter).order_by("-"+constants.CREATED_AT)

    return collection.objects(**read_filter).order_by("-"+constants.CREATED_AT)


def modify_records(collection, read_filter, update_filter):
    """
    update records based on the read filter
    :param collection:
    :param read_filter:
    :param update_filter
    :return:
    """
    update_filter[constants.UPDATED_AT] = common_utils.get_current_time()
    return collection.objects(**read_filter).modify(new=True, **update_filter)


def insert_record(collection, data):
    """
    Create records in database with respect to collection and data
    :param collection:
    :param data:
    :return:
    """
    data.update({constants.UID: str(uuid.uuid4()),
                 constants.CREATED_AT: common_utils.get_current_time(),
                 constants.UPDATED_AT: common_utils.get_current_time()})
    return collection(**data).save()


def insert_bulk_record(collection, data):
    """
    Create records in database with respect to collection
    :param collection:
    :param data:
    :return:
    """
    for item in data:
        item[constants.CREATED_AT] = common_utils.get_current_time()
        item[constants.UPDATED_AT] = common_utils.get_current_time()

    return collection.objects.insert(data)


def delete_record(collection, delete_filter):
    """
    Create records in database with respect to collection
    :param collection:
    :param delete_filter:
    :return:
    """
    return collection.objects(**delete_filter).delete()
