# General

Spelling mistakes are often fixed, but case is sometimes normalised to lowerUpper, and sometimes kept as is (e.g. "StartDate").
Prompt has now been tweaked to solve the issue in future conversions.

There is no clear root container in many of the cases.

# Per case

* HelpingHands:
  * On a first run, the reference from Route to Item has the wrong name (`pickupRoute`).
    This may be because of the source PlantUML, which does not have a direction.
  * This was fixed on a second run with the same prompt.
* Sober:
  * The "frozen" modifier from UML 1.x has not been taken into account.
* TileOGame:
  * Game has two constants in it.
  * This metamodel has significant use of custom cardinalities (besides the typical zero-to-one and zero-to-many ones).
* TransportCompany:
  * Fixed typo (e.g. "VerhicleType" -> "VehicleType").