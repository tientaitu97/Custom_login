import sys
from h3 import h3

# resolution-table
r_maps = (
    (0.000509713, 0.001348575, 15),
    (0.001348575, 0.003559893, 14),
    (0.003559893, 0.009415526, 13),
    (0.009415526, 0.024910561, 12),
    (0.024910561, 0.065907807, 11),
    (0.065907807, 0.174375668, 10),
    (0.174375668, 0.461354684, 9),
    (0.461354684, 1.220629759, 8),
    (1.220629759, 3.229482772, 7),
    (3.229482772, 8.544408276, 6),
    (8.544408276, 22.606379400, 5),
    (22.606379400, 59.810857940, 4),
    (59.810857940, 158.244655800, 3),
    (158.244655800, 418.676005500, 2),
    (418.676005500, 1107.712591000, 1),
    (1107.712591000, sys.maxsize, 0),
)


def d_to_r(d):
    """convert distance (in KM) to resolution (hash level: 0 -> 7)"""
    for min, max, val in r_maps[::-1]:
        if d >= min and d < max:
            return val


def hash(lon, lat):
    """:return tuple of hashed geo address with resolution ( hash level)"""
    return [(r, h3.geo_to_h3(lon, lat, r)) for (min, max, r) in r_maps]


def to_hash_fields(lon, lat):
    """return key-value array of hashed geo address with resolution ( hash level)"""
    hashed = hash(lon, lat)
    fields = {}
    for r, adr in hashed:
        fields.update({'h3_{0}'.format(r): adr})
    return fields


def adr_with_d(d, lon, lat):
    """return hashed geo address with search distance (in KM)"""
    r = d_to_r(d)
    adr = h3.geo_to_h3(lon, lat, r)
    return adr


if __name__ == '__main__':
    print('running geo hash..')
    r = d_to_r(123)
    print('resolution: {}'.format(r))

    hashed_fields = to_hash_fields(37.3615593, -122.0553238)
    print('hashed_fields: ', hashed_fields)

    hashed_geo_with_distance = adr_with_d(3.5, 37.3615593, -122.0553238)
    print('hashed_geo_with_distance: ', hashed_geo_with_distance)

    for k, v in hashed_fields.items():
        if v == hashed_geo_with_distance:
            print('matched with resolution = {}'.format(k))
            break
    else:
        print('not found')
