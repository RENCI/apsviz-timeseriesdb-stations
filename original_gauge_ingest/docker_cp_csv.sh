# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

docker cp dbo_GAGES_ALL.csv apsviz-timeseriesdb-db-1:/home/
docker cp noaa_stations.csv apsviz-timeseriesdb-db-1:/home/
docker cp ndbc_stations.csv apsviz-timeseriesdb-db-1:/home/
