-- SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
--
-- SPDX-License-Identifier: GPL-3.0-or-later
-- SPDX-License-Identifier: LicenseRef-RENCI
-- SPDX-License-Identifier: MIT

COPY ndbc_stations(station,lat,lon,name,units,tz,owner,state,county)
FROM '/home/ndbc_stations.csv'
DELIMITER ','
CSV HEADER;
