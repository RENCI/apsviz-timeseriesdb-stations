-- SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
--
-- SPDX-License-Identifier: GPL-3.0-or-later
-- SPDX-License-Identifier: LicenseRef-RENCI
-- SPDX-License-Identifier: MIT

CREATE TABLE IF NOT EXISTS ndbc_stations (
   ID SERIAL PRIMARY KEY,
   station VARCHAR (5) NOT NULL,
   lat FLOAT NOT NULL,
   lon FLOAT NOT NULL,
   name VARCHAR (50) NOT NULL,
   units VARCHAR (2) NOT NULL,
   tz VARCHAR (3) NOT NULL,
   owner VARCHAR (4) NULL,
   state VARCHAR (4) NULL,
   county VARCHAR (4) NULL
);
