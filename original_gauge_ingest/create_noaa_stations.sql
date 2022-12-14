-- SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
--
-- SPDX-License-Identifier: GPL-3.0-or-later
-- SPDX-License-Identifier: LicenseRef-RENCI
-- SPDX-License-Identifier: MIT

CREATE TABLE IF NOT EXISTS noaa_stations (
   ID SERIAL PRIMARY KEY,
   tidal BOOLEAN NOT NULL,
   greatlakes BOOLEAN NOT NULL,
   shefcode VARCHAR (5) NULL,
   state VARCHAR (19) NULL,
   timezone VARCHAR (3) NOT NULL,
   timezonecorr INT NOT NULL,
   observedst BOOLEAN NOT NULL,
   stormsurge BOOLEAN NOT NULL,
   forecast BOOLEAN NOT NULL,
   nonNavigational BOOLEAN NOT NULL,
   station_name VARCHAR (7) NOT NULL,
   name VARCHAR (40) NOT NULL,
   lat FLOAT NOT NULL,
   lon FLOAT NOT NULL,
   affiliations VARCHAR (27) NULL,
   portscode VARCHAR (4) NULL,
   self VARCHAR (77) NOT NULL,
   expand VARCHAR (86) NOT NULL,
   tideType VARCHAR (13) NOT NULL,
   details VARCHAR (85) NOT NULL,
   sensors VARCHAR (85) NOT NULL,
   floodlevels VARCHAR (89) NOT NULL,
   datums VARCHAR (84) NOT NULL,
   supersededdatums VARCHAR (94) NOT NULL,
   harmonicConstituents VARCHAR (84) NOT NULL,
   benchmarks VARCHAR (88) NOT NULL,
   tidePredOffsets VARCHAR (93) NOT NULL,
   nearby VARCHAR (84) NOT NULL,
   products VARCHAR (86) NOT NULL,
   disclaimers VARCHAR (89) NOT NULL,
   notices VARCHAR (85) NOT NULL
);