#!/bin/bash
#Run as root user
#dependencies tar, pigz

su - postgres -c 'pg_dump -f galaxy_tools.psql galaxy_tools'
echo "DUMP: psql file created"
mkdir -p /tmp/dump
mv /var/lib/pgsql/galaxy_tools.psql /tmp/dump/dump.psql
cp /home/galaxy/galaxy/config/shed_tool_conf.xml /tmp/dump
echo "DUMP: psql file and shed_tool conf file moved to /tmp/dump"
tar cvzf --use-compress-program=pigz /tmp/dump/tar_shed_tools.tar.gz /home/galaxy/galaxy/var/shed_tools/ &
tar cvzf --use-compress-program=pigz /tmp/dump/tar_conda.tar.gz /export/tool_deps/_conda &
wait
echo "DUMP: tar_conda.tar.gz created"
echo "DUMP: tar_shed_tools.tar.gz created"
echo "DUMP: DONE"

