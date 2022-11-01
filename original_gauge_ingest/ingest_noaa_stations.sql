-- SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
--
-- SPDX-License-Identifier: GPL-3.0-or-later
-- SPDX-License-Identifier: LicenseRef-RENCI
-- SPDX-License-Identifier: MIT

COPY noaa_stations(tidal,greatlakes,shefcode,state,timezone,timezonecorr,observedst,stormsurge,forecast,nonNavigational,station_name,name,lat,lon,affiliations,portscode,self,expand,tideType,details,sensors,floodlevels,datums,supersededdatums,harmonicConstituents,benchmarks,tidePredOffsets,nearby,products,disclaimers,notices)
FROM '/home/noaa_stations.csv'
DELIMITER ','
CSV HEADER;
