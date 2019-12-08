#!/bin/bash

GN_PATH="$1"

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"


. $GN_PATH/config/settings.ini

LOG_FILE="$GN_PATH/var/log/install_monitoring_chiro.log"

echo "Create chiro schema..." > $LOG_FILE
echo "--------------------" &>> $LOG_FILE
echo "" &>> $LOG_FILE
export PGPASSWORD=$user_pg_pass;psql -h $db_host -p $db_port -U $user_pg -d $db_name -f $SCRIPTPATH/data/schema_chiro.sql  &>> $LOG_FILE


echo "Import chiro data" &>> $LOG_FILE
echo "--------------------" &>> $LOG_FILE
echo "" &>> $LOG_FILE
export PGPASSWORD=$user_pg_pass;psql -h $db_host -p $db_port -U $user_pg -d $db_name -f $SCRIPTPATH/data/data_chiro.sql  &>> $LOG_FILE

echo "Create chiro views" &>> $LOG_FILE
echo "--------------------" &>> $LOG_FILE
echo "" &>> $LOG_FILE
export PGPASSWORD=$user_pg_pass;psql -h $db_host -p $db_port -U $user_pg -d $db_name -f $SCRIPTPATH/data/views.sql  &>> $LOG_FILE
