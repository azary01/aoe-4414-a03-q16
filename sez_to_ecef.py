# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts sez coordinates to ecef coordinates
# Parameters:
#  o_lat_deg: lattitude in degrees of the ground station
#  o_lon_deg: longitude in degrees of the ground station
#  o_hae_km: height above elipsoid in km of the ground station
#  s_km: South coordinate in km of the object from the ground station
#  e_km: East coordinate in km of the object from the ground station
#  z_km: Z coordinate in km of the object from the ground station
# Output:
#  Print the ecef coordinates (r_x_km, r_y_km, r_z_km) of the given sez location
#
# Written by: Austin Zary
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import math # math module
import sys # argv

# "constants"
R_E_KM = 6378.1363
E_E    = 0.081819221456

# helper functions

## calc_denom
##
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-ecc**2.0 * math.sin(lat_rad)**2.0)

# initialize script arguments
o_lat_deg = float('nan') # latitude in degrees
o_lon_deg = float('nan') # longitude in degrees
o_hae_km = float('nan') # height above ellipsoid in km
s_km = float('nan') # South coordinate in km of the object from the ground station
e_km = float('nan') # East coordinate in km of the object from the ground station
z_km = float('nan') # Z coordinate in km of the object from the ground station

# parse script arguments
if len(sys.argv)==7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg = float(sys.argv[2])
  o_hae_km = float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 arg1 arg2 arg3 ...'\
  )
  exit()

# Rotate SEZ coordinates to ECEF coordinates measured from ground station
o_lat_rad = o_lat_deg*math.pi/180.0
o_lon_rad = o_lon_deg*math.pi/180.0

local_r_x = math.cos(o_lon_rad)*math.sin(o_lat_rad)*s_km + math.cos(o_lon_rad)*math.cos(o_lat_rad)*z_km - math.sin(o_lon_rad)*e_km
local_r_y = math.sin(o_lon_rad)*math.sin(o_lat_rad)*s_km + math.sin(o_lon_rad)*math.cos(o_lat_rad)*z_km + math.cos(o_lon_rad)*e_km
local_r_z = -math.cos(o_lat_rad)*s_km + math.sin(o_lat_rad)*z_km

# Translate local relative ECEF coordinates to global ECEF coordinates
denom = calc_denom(E_E, o_lat_rad)
c_e = R_E_KM/denom
s_e = R_E_KM*(1.0-E_E**2.0)/denom

ground_r_x = (c_e+o_hae_km)*math.cos(o_lat_rad)*math.cos(o_lon_rad)
ground_r_y = (c_e+o_hae_km)*math.cos(o_lat_rad)*math.sin(o_lon_rad)
ground_r_z = (s_e+o_hae_km)*math.sin(o_lat_rad)

r_x_km = local_r_x + ground_r_x
r_y_km = local_r_y + ground_r_y
r_z_km = local_r_z + ground_r_z

print(r_x_km)
print(r_y_km)
print(r_z_km)