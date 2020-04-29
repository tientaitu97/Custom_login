import base64
import csv
from datetime import datetime
import json
import os
import time
import zipfile

from django.conf import settings
from django.utils.text import slugify
from pytz import reference

from config.settings.default import BASE_DIR

default_limit = 20


def get_date_now():
    return 'date'


def get_now():
    now = datetime.now().replace(tzinfo=reference.LocalTimezone())
    return now


# return access token
def get_access_token(request):
    try:
        return request.auth.decode()
    except AttributeError:
        return None


def decode_authorization(request):
    try:
        basic_auth = request.META['HTTP_AUTHORIZATION']
        basic_token = basic_auth.split(' ')[1]
        basic_token_encode = base64.b64decode(basic_token).decode()
        user_name = basic_token_encode.split(':')[0]
        password = basic_token_encode.split(':')[1]
        return user_name, password
    except:
        return None, None


# get epoch time now
def get_epoch_time_now():
    return time.time()


def today():
    return datetime.date.today


# get all fields of model
def get_model_fields(model):
    return model._meta.fields


# convert gen csv file from model
def model_to_csv(model, data, work_dir=None):
    current_work_dir = settings.MEDIA_ROOT if not work_dir else work_dir
    epoch_now = get_epoch_time_now()
    model_verbose_name = model._meta.verbose_name
    file_name = os.path.join(current_work_dir, '{}_{}.csv'.format(model_verbose_name, epoch_now))

    # fields of model
    fields = get_model_fields(model)

    # write csv file
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        # write your header first
        field_names = [field.verbose_name for field in fields]
        writer.writerow(field_names)
        # write data
        for row in data:
            writer.writerow(row)
    return file_name


# method archive a file
def zip_afile(file_path, work_dir=None):
    current_work_dir = settings.MEDIA_ROOT if not work_dir else work_dir
    csv_file = os.path.basename(file_path)
    file_name = os.path.join(current_work_dir, '{}.zip'.format(csv_file))
    # write a zip file
    with zipfile.ZipFile(file_name, 'w') as zip:
        zip.write(file_path, csv_file, compress_type=zipfile.ZIP_DEFLATED)
    return file_name


def get_unique_slug(model_instance, slugable_field_name, slug_field_name):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    model_class = model_instance.__class__

    while model_class._default_manager.filter(
            **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = '{}-{}'.format(slug, extension)
        extension += 1

    return unique_slug


def get_price_setting(model_instance, price_filed):
    pass


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_path_category(instance, filename):
    new_filename = time.time()
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "category/image/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


# get now epoch tiem
def get_epoch_now():
    return time.time()


def listed_time_to_string(listed_time):
    now = get_epoch_time_now()
    delta_time = datetime.datetime.fromtimestamp(now) - datetime.datetime.fromtimestamp(listed_time)
    days = delta_time.days
    hours = delta_time.seconds // 3600
    minutes = (delta_time.seconds // 60) % 60
    if days > 0:
        time_string = '{} ngày trước'.format(days)
    elif hours > 0:
        time_string = '{} giờ trước'.format(hours)
    elif minutes == 0:
        time_string = 'vừa xong'
    else:
        time_string = '{} phút trước'.format(minutes)
    return time_string


# load mapping fields
def load_mapping():
    data_path = os.path.join(os.path.dirname(BASE_DIR), 'data')
    file_path = os.path.join(data_path, 'mapping.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


# load mapping fields
def load_filter_types():
    data_path = os.path.join(os.path.dirname(BASE_DIR), 'data')
    file_path = os.path.join(data_path, 'filter_types.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data


def query_key_mapping(queries):
    queries_mapping = {}
    mapping_data = load_mapping()
    for key, value in queries.items():
        appended_key = key
        for key_mapping, value_mapping in mapping_data.items():
            if key in value_mapping:
                appended_key = key_mapping
                break
        queries_mapping[appended_key] = queries.getlist(key)

    return queries_mapping


def get_key_range(key):
    range_fields = ["rooms", "mileage", "mf_date", "reg_date"]
    if key in range_fields:
        return '{}.value'.format(key)
    return key


def build_query(queries):
    filters = []
    range_fields = ["rooms", "mileage", "mf_date", "reg_date", "price"]
    queries_mapping = query_key_mapping(queries)
    for key, value in queries_mapping.items():
        if key == 'title':
            filters.append({"multi_match": {"query": value, "fields": ["title", "body"]}})
            continue
        if key == 'g_category':
            filter_key = 'category.code'
            filters.append({"match": {filter_key: value[0]}})
            continue

        if key == 's_category':
            filter_key = 'category.global_category'
            filters.append({"match": {filter_key: value[0]}})
            continue

        if key == 'listed_time':
            continue

        if key in range_fields:
            filter_key = get_key_range(key)
            for v in value:
                filters.append({"range": {filter_key: {"gte": v}}})
            continue
        if type(value) is list:
            filter_key = '{}.value'.format(key)
            for v in value:
                filters.append({"match": {filter_key: v}})
            continue

    dict_query = {"query": {"bool": {"must": filters}}}
    return dict_query


def has_next(current_page, total):
    total_page = get_num_pages(total)
    if current_page < total_page:
        return True
    return False


def get_next_page(page, total):
    total_pages = get_num_pages(total)
    if page >= total_pages:
        return None
    return page + 1


def get_prev_page(page, total):
    total_pages = get_num_pages(total)
    if page <= 1 or total_pages == 1:
        return None
    return page - 1


def get_num_pages(total):
    total_page = (total // default_limit) if total % default_limit == 0 else (total // default_limit + 1)
    return total_page


def get_offset(page, total):
    total_page = get_num_pages(total)
    if page > total_page:
        page = total_page
    start_offset = ((page - 1) * default_limit) + 1
    end_offset = page * default_limit
    return start_offset, end_offset
