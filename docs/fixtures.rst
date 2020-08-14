.. _fixtures:


Fixtures example
================



Fixture file structure
----------------------

Save fixture in json file with following structue.

Custodian
^^^^^^^^^

Set target to "custodian". Set type for every fixture, it can be migration or record.
Use following structure.

.. code-block:: bash

    [
        {
            "target": "custodian",
            "fixture":[
                {
                    "type": "migration",
                    "migration": {
                        "applyTo": "",
                        "operations": [
                            {
                                "object": {
                                    "cas": false,
                                    "fields": [ ... ],
                                    "name": "contacts_type",
                                    "key": "id"
                                },
                                "type": "createObject"
                            }
                        ],
                        "id": <id>,
                        "dependsOn": []
                    }
                }, 
                {
                    "type": "record",
                    "object": "contacts_type",
                    "data": [ ... ]
                }
            ]
        }
    ]


Authorization/Fileservice
^^^^^^^^^^^^^^^^^^^^^^^^^

Set target to "authorization/fileservice". Type of every fixture should be a record.
Use following structure.

.. code-block:: bash

    [
        {
            "target": <authorization/fileservice>,
            "fixture": [
                {
                    "model": <model.name>,
                    "pk": <id>,
                    "fields": { ... }
                }
            ]
        }
    ]
