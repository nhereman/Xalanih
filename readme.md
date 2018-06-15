# Technical Requirements
- Python 3.6

# How to use Xalanih

#### Create the db
```
python3 xalanih create
```

#### Update the db
```
python3 xalanih update
```
# How to structure the directory containing the database scripts

The structure to use for the directory that contains all the scripts you have for your database.

```
L creation (directory)
    L  creation.ddl (file)
    L  included_updates (file)
L update (directory)
    L  script01.ddl (file)
    L  ...
```

## creation *(directory)*
The **creation** directory will contains the scripts that will be used to create the baseline of the database. These will only be called when the database is created from zero. That means that they will not be used in case of a database update.

### creation.ddl *(file)*
The script **creation.ddl** is the entrypoint of Xalanih to create the database. This file must contains all the needed script to create the baseline of your database.

### included_updates *(file)*
When you will have a lot of update file, you will want to create the database directly with these modification instead of applying them after. In order to do that, you will have to add the modification directly to your *creation.ddl*. But in order for Xalanih to not apply the update scripts, you have to add the name of all update scripts already integrated to the file **included_updates**. There should be one filename by line.

## update *(directory)*
The **update** directory must contains all your update scripts (and nothing else). There is not realy a nomenclature for the update scripts but the alphabetical order should correspond to their chronological order.