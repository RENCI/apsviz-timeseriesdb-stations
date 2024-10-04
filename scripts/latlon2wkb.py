from shapely import wkb, wkt
g = wkt.loads('POINT(-81.7883333333 26.1366666667)')
wkb.dumps(g, hex=True, srid=4326)
