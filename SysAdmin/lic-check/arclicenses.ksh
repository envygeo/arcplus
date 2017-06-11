#!/bin/ksh
#Luke Pinner, April 2005
# --------------------------------
# Usage and Arguments
# --------------------------------
my_name=$(basename $0)
Usage="Checks ESRI license usage\nUsage:${my_name} [-f feature] [-s port@server] [-q] [-h]\n"

#Vars
ARCHOME=/sw/esri/arcinfo/9.0/arcexe9x

#Defaults
FEATURE=ARC/INFO
PORT_SERVER=server@port
SHHH=0

#Args
while getopts hqf:s: c ; do
  case $c in
    h)	echo ${Usage} ; exit 0 ;;
    q)	SHHH=1 ;;
    f)	FEATURE=$OPTARG ;;
    s)	PORT_SERVER=$OPTARG ;;
    \?) echo ${Usage} ; exit 1 ;;
  esac
done
shift `expr $OPTIND - 1`

#Strip out the 3rd field returned by a grep of the license info from lmutil lmstat -i
#
#Format returned by lmutil lmstat -i is:
#
#Feature                 Version   #licenses    Expires         Vendor
#--------                -------   ----------    ---------       ------
#ARC/INFO                9.0           8         01-jan-00       ARCGIS
#
# $1=varname $2=Feature $3=Version $4=#licenses etc...
set license `$ARCHOME/sysgen/lmutil lmstat -i "$FEATURE" | grep -i "^${FEATURE}"`
TOTAL=$4

#Get number of licenses in use
#"start" is a good pattern to use for the grep - it only occurs in license usage lines 
#and not the other lines returned by lmutil lmstat
#eg.     username computername {}ueqn{#{QjH!cM2c (v9.0) (server/port 5157), start Thu 3/31 12:25
USED=`$ARCHOME/sysgen/lmutil lmstat -f "$FEATURE" -c "$PORT_SERVER" | grep -c start`

#Get number of licenses available
((AVAIL = TOTAL - USED))

#What goes to STDOUT
if test $SHHH -eq 0
then
  echo $TOTAL $FEATURE licences in total
  echo $USED $FEATURE licences are in use
  echo $AVAIL $FEATURE licences are available
else
  echo $AVAIL
fi

#Some license names:
# ARC/INFO
# Plotting
# Network
# TIN
# Interop
# Grid
# ArcScan
# Publisher
# ArcPress
# Viewer
# GeoStats
# Editor
