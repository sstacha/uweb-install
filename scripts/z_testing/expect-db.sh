#! /usr/bin/expect
#
# tries to turn off autocommit and such for mysql before doing import to improve the 10min time for import
spawn mysql -h localhost -u root --password=root --protocol tcp django
expect "mysql>" 
send "set autocommit=0;\r" 
expect "mysql>"
send "SET unique_checks=0;\r" 
expect "mysql>"
send "SET foreign_key_checks=0;\r" 
expect "mysql>"
send "SOURCE django.mysqlprod.spe.org.sql;\r"
expect "mysql>"
send "COMMIT;\r"
expect "mysql>"
send "set autocommit=1;\r" 
expect "mysql>"
send "SET unique_checks=1;\r" 
expect "mysql>"
send "SET foreign_key_checks=1;\r" 
