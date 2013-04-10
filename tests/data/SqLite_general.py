#
# These are the tests for the SqLite module. they will test the basic
# functionality.
# I didn't use any test suits because I didn't know any libraries in python
# and I didn't have enough time.

from sys import path

# add the lib to path
#path.append("../../")

from data.SqLite import *

print("Starting tests, things should run without errors")
sq1 = SqLite("test")
sq1.setNamespace("test1")

if sq1.hasNamespace():
    sq1.removeNamespace()
    print("Removed old test database.")

table_def = {"field1":"TEXT", "field2":"INTEGER", "field3":"BLOB"}

print("Installing namespace")
sq1.installNamespace("test1", table_def)

if not sq1.hasNamespace():
    print("ERROR: was not able to create database")
    
sq1.write({"field1":"Test Value 1", "field2":100, "field3":"something"})

many_writes = [
               {"field1":"Test Value 2", "field2":200, "field3":"something 2"},
               {"field1":"Test Value 3", "field2":300, "field3":"something 3"},
               {"field1":"Test Value 4", "field2":400, "field3":"something 4"},
               {"field1":"Test Value 5", "field2":500, "field3":"something 5"},
               {"field1":"Test Value 6", "field2":600, "field3":"something 6"}]

sq1.writeMany(many_writes)

cond = C.Or(
            C.And(
             C._("field2", ">", 200),
             C._("field2", "<", 600)
             ),
            C._("field1", "=", "Test Value 2")
            )

sq1.search(cond)

result = sq1.read()

if len(result) != 4:
    print("ERROR: either rows where not added or searcg doesn't work")
    
print ("Test of value: " + result[0]["field1"])

sq1.deleteOne(2)

sq1.search(C._("id", "=", 2))

result = sq1.read()

if result:
    print ("ERROR: Could not remove the row.")
    
sq1.deleteMany([2,3,4])

sq1.search(C._raw("id", "IN", "(2,3,4)"))

result = sq1.read()

if result:
    print ("ERROR: Could not remove multiple rows.")