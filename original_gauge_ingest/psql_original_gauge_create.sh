#!/bin/bash

# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

source .env.db

PGPASSWORD=$POSTGRES_PASSWORD psql -U apsviz_gauges -d apsviz_gauges -p 5432 -h localhost -f create_dbo_GAGES_ALL.sql
PGPASSWORD=$POSTGRES_PASSWORD psql -U apsviz_gauges -d apsviz_gauges -p 5432 -h localhost -f create_noaa_stations.sql
PGPASSWORD=$POSTGRES_PASSWORD psql -U apsviz_gauges -d apsviz_gauges -p 5432 -h localhost -f create_ndbc_stations.sql
