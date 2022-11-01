#!/bin/bash

# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

# setup specific to apsviz_timeseriesdb_stations
version=$1;

docker network connect apsviz-timeseriesdb_default apsviz_timeseriesdb_stations_$version
