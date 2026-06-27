# General

Spelling mistakes are often fixed, but case is sometimes normalised to lowerUpper, and sometimes kept as is (e.g. "StartDate").

There is no clear root container in many of the cases.

# Per case

* Facepage:
  - Privilege not converted to association class.
  - FriendRequest not reachable from PersonalAccount.
* HelpingHands:
  - Can't get to Route from Item.
* HomeForTheElderly:
  - Bed.person is redundant given the Proposal association class.
  - Same goes for Person.bed.
* House:
  * JobLog isn't visible from House and Company.
* LabTracker:
  * Appointment is redundantly expressed between Lab and Requisition.
* Menso:
  * TripDateTime has been left as just a string instead of a timestamp.
* MusicMatic:
  * The Track association class isn't directly accessible from Hit nor from Album.
* PizzaRestaurant:
  * The Employment association class was correctly done in this case, without explicit prompting.
* School:
  * TeacherAssignment class is modelled redundantly between Teacher and School (Teacher has references to both the School and the TeacherAssignment, and School has references to both Teacher and TeacherAssignment).
* Sightseeing:
  * Discount association class is redundantly modelled.
* Sober:
  * The "frozen" modifier has not been taken into account.
  * numberOfCustomers() in RideSharing has been dropped.
  * Customer operations have also been dropped.
  * Involved association class is not accessible from Car nor Accident.
* StudentAppointment:
  * The two association classes were correctly transformed in this case.
* TileOGame:
  * Game has two constants in it.
  * This metamodel has significant use of custom cardinalities (besides the typical zero-to-one and zero-to-many ones).
* TransportCompany:
  * Vehicle.orders has + cardinality even though the diagram only says "*".
  * Order.StartTime and Order.EndTime are just strings, instead of times.
  * Fixed typo (e.g. "VerhicleType" -> "VehicleType").
* University:
  * Participation association class is redundantly modelled.