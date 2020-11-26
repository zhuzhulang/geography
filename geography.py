# encoding:utf-8
from __future__ import unicode_literals
from six.moves.urllib_request import urlopen
from ipdb import City
from os import path
import re
import json

CURRENT_DIRECTORY = path.dirname(path.abspath(__file__))
IP_REGEXP = "\d+\.\d+\.\d+\.+\d+"
IP_DATABASE_PATH = path.join(CURRENT_DIRECTORY, "ipipfree.ipdb")
LOCATION_FILENAME = path.join(CURRENT_DIRECTORY, "geography.json")
LOCATION_URL = "http://ip-api.com/json/"
LOCATION_DICT = None  # 地址字典
pattern = re.compile(IP_REGEXP)


def _get_location_by_ip(ip):
    """
    根据IP获取经纬度
    :param ip:
    :return:
    """
    url = LOCATION_URL + str(ip)
    keys = ["lon", "lat"]
    result = []
    try:
        req = urlopen(url)
    except Exception as e:
        print("ERROR", e)
        print(url)
        data = "{}"
    else:
        data = req.read()
        _result = json.loads(data)
        for key in keys:
            c = _result.get(key)
            if c is None:
                c = -1
            result.append((key, c))
    finally:
        return dict(result)


def get_ip_info(ip, location_dict):
    """
    获取指定IP的信息
    :param ip:
    :return:
    """
    info = {}
    if path.exists(IP_DATABASE_PATH):
        if ip:
            db = City(IP_DATABASE_PATH)
            _ip = pattern.search(ip)
            if _ip:
                ip = _ip.group()
            if isinstance(ip, bytes):
                ip = ip.decode("utf-8")
            if ip:
                info = db.find_map(ip, "CN")
                key = "{}{}".format(info.get("region_name", ""), info.get("city_name", ""))
                val = location_dict.get(key)
                if val is None:
                    location = _get_location_by_ip(ip)
                else:
                    location = val
                info.update(location)
    else:
        print("IP Database file is not found...")
    return info


def get_address_latitude():
    """
    获取地址的经纬度
    :return:
    """
    if path.exists(LOCATION_FILENAME):
        with open(LOCATION_FILENAME, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    return data


def get_last_ip_info(ip):
    """
    获取处理后的IP信息
    :param id_list:
    :return:
    """
    global LOCATION_DICT
    if LOCATION_DICT is None:
        LOCATION_DICT = get_address_latitude()
    ip_info = get_ip_info(ip, LOCATION_DICT)
    if ip_info:
        lat = ip_info.get("lat", -1)  # 纬度
        lon = ip_info.get("lon", -1)  # 经度
        lat = round(float(lat), 3)
        lon = round(float(lon), 3)
        location = "{},{}".format(lon, lat)
    else:
        location = ""
    fields = ["country_name", "region_name", "city_name"]
    geo = []
    for field in fields:
        val = ip_info.get(field, "")
        if val not in geo:
            geo.append(val)
    geo_str = "".join(geo)  # IP来源地址
    record = {"geo": geo_str, "location": location}
    return record
