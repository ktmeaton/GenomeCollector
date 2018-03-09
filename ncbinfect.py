#!/usr/bin env python
"""
Created on Thurs Mar 08 2018

@author: Katherine Eaton

"NCBInfect Main Program"
"""

# This program should only be called from the command-line
if __name__ != "__main__": quit()

import argparse
import sqlite3
import os
import sys
from Bio import Entrez
from xml.dom import minidom
import xml.etree.cElementTree as ElementTree

src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '') + "src"
sys.path.append(src_dir)

import NCBInfect_Utilities
import NCBInfect_Errors


#-----------------------------------------------------------------------#
#                            Argument Parsing                           #
#-----------------------------------------------------------------------#

# To Be Done: Full Description
parser = argparse.ArgumentParser(description='Description of NCBInfect.',
                                 add_help=True)


# Argument groups for the program
mandatory_parser = parser.add_argument_group('mandatory')

mandatory_parser.add_argument('--outputdir',
                    help = 'Output directory.',
                    action = 'store',
                    dest = 'outputDir',
					required = True)

parser.add_argument('--config',
                    help = 'Path to configuration file "config.py".',
                    action = 'store',
                    dest = 'configPath',
					required = True)

parser.add_argument('--flat',
                    help = 'Do not create organization directories, output all files to output directory.',
                    action = 'store_true',
                    dest = 'flatMode')



# Retrieve user parameters
args = vars(parser.parse_args())

config_path = args['configPath']
output_dir = args['outputDir']
flat_mode = args['flatMode']



#------------------------------------------------------------------------------#
#                              Argument Parsing                                #
#------------------------------------------------------------------------------#

# Check if config.py file exists
if not os.path.exists(config_path):
	raise ErrorConfigFileNotExists(config_path)

# Add the directory containing config.py to the system path for import
sys.path.append(os.path.dirname(config_path))
import config as CONFIG

print(
"\n" + "NCBInfect run with the following options: " + "\n" +
"\t" + "Output Directory: " + CONFIG.OUTPUT_DIR + "\n" +
"\t" + "Email: " + CONFIG.EMAIL + "\n" +
"\t" + "User Database: " + str(CONFIG.DATABASE) + "\n" +
"\t" + "Tables: " + str(CONFIG.TABLES) + "\n" +
"\t" + "Search Terms: " + str(CONFIG.SEARCH_TERMS) + "\n\n")

# Flat mode checking
if flat_mode:
	print("Flat mode was requested, organizational directories will not be used.")
	DB_DIR = os.path.join(output_dir, "")
	LOG_PATH = output_dir


elif not flat_mode:
	# Create accessory directory (ex. log, data, database, etc.)
	print("Flat mode was not requested, organization directories will be used.")
	NCBInfect_Utilities.check_accessory_dir(output_dir)
	DB_DIR = os.path.join(output_dir, "", "database", "")
	LOG_PATH = os.path.join(output_dir, "", "log")

DB_PATH = os.path.join(DB_DIR, "", CONFIG.DATABASE)

#------------------------- Database Connection---------------------------------#
if not os.path.exists(DB_PATH):
	print('\nCreating database: ' + DB_PATH)
	conn = sqlite3.connect(DB_PATH)
	conn.commit()
	print('\nConnected to database: ' + DB_PATH)

elif os.path.exists(DB_PATH):
	conn = sqlite3.connect(DB_PATH)
	conn.commit()
	print('\nConnected to database: ' + DB_PATH)

#------------------------------------------------------------------------------#
#                       Database Processing Function                           #
#------------------------------------------------------------------------------#

def UpdateDB(table, output_dir, database, email, search_term, table_columns, log_path, db_dir):
	print("\nCreating/Updating the", table, "table using the following parameters: " + "\n" +
	"\t" + "Database: " + "\t\t" + database + "\n" +
	"\t" + "Search Term:" + "\t" + "\t" + search_term + "\n" +
	"\t" + "Email: " + "\t\t\t" + email + "\n" +
    "\t" + "Output Directory: "	 + "\t" + output_dir + "\n\n")


	Entrez.email = email

    #---------------------------------------------------------------------------#
    #                                File Setup                                 #
    #---------------------------------------------------------------------------#
    # Name of Log File
	log_file_path = os.path.join(LOG_PATH, "",
								os.path.splitext(database)[0] + "_" + table + ".log")

	# Check if the file already exists, either write or append to it.
	if os.path.exists(log_file_path):
		log_file = open(log_file_path, "a")
	else:
		log_file = open(log_file_path, "w")

    #--------------------------------------------------------------------------#
    #                                SQL Setup                                 #
    #--------------------------------------------------------------------------#

	# Connect to database and establish cursor for commands.
	conn = sqlite3.connect(os.path.join(db_dir, "", database))
	cur = conn.cursor()

    ## Create the database
    # Check if strain is in table
	sql_query = ("Create TABLE IF NOT EXISTS " + table +
	" (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " +
	table + "_id TEXT")
	for column in table_columns:
		if type(column) == tuple or type(column) == list:
			 column = column[0]
		# By default, every user-specified column is type TEXT
		sql_query += ", " + column + " TEXT"
	sql_query += ")"

	cur.execute(sql_query)

	#-----------------------------------------------------------------------#
	#                          Entrex Search                                #
	#-----------------------------------------------------------------------#

	handle = Entrez.esearch(db=table.lower(),
                            term=search_term,
                            retmax = 1)

	# Read the record, count total number entries, create counter
	record = Entrez.read(handle)
	num_records = int(record['Count'])
	num_processed = 0

	#-----------------------------------------------------------------------#
	#                          Iterate Through ID List                      #
	#-----------------------------------------------------------------------#

	for ID in record['IdList']:
		#-------------------Progress Log and Entry Counter-------------------#
		# Increment entry counter and record progress to screen
		num_processed += 1
		print("Processing record: " +
	   		str(num_processed) + \
	   		"/" + str(num_records))

        #------------Check if Record Already Exists in Database------------#

		sql_query = ("SELECT EXISTS(SELECT " + table + "_id FROM " +
					table + " WHERE " + table + "_id=?)")

		cur.execute(sql_query, (ID,))

        # 0 if not found, 1 if found
		record_exists = cur.fetchone()[0]

		if record_exists:
			continue
		'''
        IMPORTANT:
        The ID should not exists in the table UNLESS the record was fully parsed.
        ie. The database does not get updated until the end of each record.
        '''

		#---------------If Assembly Isn't in Database, Add it------------#
		# Retrieve Assembly record using ID, read, store as dictionary
		ID_handle = Entrez.esummary(db=table.lower(),id=ID)
		ID_record = Entrez.read(ID_handle, validate=False)
		record_dict = ID_record['DocumentSummarySet']['DocumentSummary'][0]
		flatten_record_dict = list(NCBInfect_Utilities.flatten_dict(record_dict))
		column_dict = {}



		for column in table_columns:
			column_value = ""

			# Attempt 1: Simple Dictionary Parse, taking first match
			for row in flatten_record_dict:
				if column in row:
					column_value = row[-1]
					break

			if column_value:
				column_dict[column] = column_value
				continue

			# Attempt 2: XML Parse
			for row in flatten_record_dict:
				result = [s for s in row if column in s]
				if not result: continue
				result = result[0].strip()
				if result[0] != "<" or result[-1] != ">": continue
				# Just in case, wrap sampledata in a root node for XML formatting
				xml = "<Root>" + result + "</Root>"
				#print(xml)
		        # minidom doc object for xml manipulation and parsing
				root = minidom.parseString(xml).documentElement
				for child in root.childNodes:
					for child in child.childNodes:
						print(type(child))
						print(child.toxml())
						if child.firstChild: print(child.firstChild.nodeValue)
					break


			column_dict[column] = column_value

		#print(column_dict)

	# CLEANUP
	conn.commit()
	cur.close()
	log_file.close()


#------------------------Iterate Through Tables--------------------------------#

for table in CONFIG.TABLES:
	OUTPUT_DIR = CONFIG.OUTPUT_DIR
	DATABASE = CONFIG.DATABASE
	EMAIL = CONFIG.EMAIL
	SEARCH_TERM = CONFIG.SEARCH_TERMS[table]
	TABLE_COLUMNS = CONFIG.TABLE_COLUMNS[table]
	UpdateDB(table, OUTPUT_DIR, DATABASE, EMAIL, SEARCH_TERM, TABLE_COLUMNS, LOG_PATH, DB_DIR)
