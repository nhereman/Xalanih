##-*- coding: utf-8 -*-
import argparse

class Parameters:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Xalanih: Database versioning helper.")
        # Action param
        self.parser.add_argument("action",
                choices=["create", "update"],
                help="Give the action to execute. create: Create the database\
                from zero. update: execute the needed update scripts on an existing database")

        # DB files directory
        self.parser.add_argument("-d","--directory",
                dest= "directory",
                default=".")
                
        self.args = self.parser.parse_args()

    def getArguments(self):
        return self.args

    def getAction(self):
        return self.args.action

    def getDirectory(self):
        return self.args.directory
