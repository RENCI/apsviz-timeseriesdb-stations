#!/bin/bash

# SPDX-FileCopyrightText: 2022 Renaissance Computing Institute. All rights reserved.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-License-Identifier: LicenseRef-RENCI
# SPDX-License-Identifier: MIT

# setup specific to apsviz_timeseriesdb_stations 
version=$1;

docker run -ti --name apsviz_timeseriesdb_stations_$version \
  --volume /Users/jmpmcman/Work/Surge/data:/data \
  -d apsviz_timeseriesdb_stations:$version /bin/bash 
