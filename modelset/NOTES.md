# General

Spelling mistakes are often fixed, but case is sometimes normalised to lowerUpper, and sometimes kept as is (e.g. "StartDate").

There is no clear root container in many of the cases.

# Per case

* HelpingHands:
  - Can't get to Route from Item.
* Menso:
  * TripDateTime has been left as just a string instead of a timestamp.
* Sober:
  * The "frozen" modifier has not been taken into account.
  * numberOfCustomers() in RideSharing has been dropped.
  * Customer operations have also been dropped.
* TileOGame:
  * Game has two constants in it.
  * This metamodel has significant use of custom cardinalities (besides the typical zero-to-one and zero-to-many ones).
* TransportCompany:
  * Vehicle.orders has + cardinality even though the diagram only says "*".
  * Order.StartTime and Order.EndTime are just strings, instead of times.
  * Fixed typo (e.g. "VerhicleType" -> "VehicleType").