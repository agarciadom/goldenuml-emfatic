# General

Spelling mistakes are often fixed, but case is sometimes normalised to lowerUpper, and sometimes kept as is (e.g. "StartDate").
Prompt has now been tweaked to solve the issue in future conversions.

There is no clear root container in many of the cases.

# Per case (first batch before rerun for general container class)

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

# Per case (second batch after rerun for general container class)

* AirTravel:
  * Employee not contained anywhere (should be in Airline).
* BankAccount:
  * Customer not contained anywhere (should be in a new top-level container).
* Boeing:
  * Employee inside AirlineRegistry instead of Airline.
* CardGameApp:
  * Identifiers written as `iD`.
* CelO:
  * Organizer.events has `+` cardinality even though it's `*` in PlantUML.
* ClothingCompany:
  * Everything contained in the same container, everything else uses non-containment refs.
  * Representative and Customer don't have a way to access their Orders.
* Ebike:
  * Everything contained in the same container, everything else uses non-containment references.
* eHome2020:
  * The incorrect containment reference from `Room` to `Apartment` is correctly flipped by Claude.
* EUScienceConnect:
  * Author is in the root container, where it could have been in Person or in Journal.
* Facepage:
  * Privilege is in the root container, where it could have been in PersonalAccount or PersonalPage.
  * PersonalPage does not have a separate association to the administrator PersonalUser - there seems to have been a confusion between the association with an association class and the one without an association class.
* FilmSet:
  * ScreenplayAuthor.createdScreenplays has `+` cardinality even though it's `*` in PlantUML.
* FitnessCompanyConan:
  * FitnessCenterModel has a redundant `trainers` containment feature (since it already has one for `persons`).
* HelpingHands:
  * Pickup / drop-off routes are modelled in the wrong direction (from Route to Item, rather than the other way).
  * Dates are contained in the root container, rather than where they are used (`Volunteer` and `Route`).
* HomeForTheElderly:
  * Association class `Proposal` is contained in the root container, rather than in one of its ends.
* Kinepolis:
  * AlternativeOffer contained in `OnlineTicket` (should be in `Show`), although this is hard to know from just the PlantUML sources.
* LabTracker:
  * Enum literals all set to `0` (this is an artifact of the Ecore-to-Emfatic conversion, not the LLM).
* LabTracker:
  * PersonRole should be contained in Person rather than in the root container.
  * Requisition points to both Lab and Appointment (redundant).
  * Lab points to both Requisition and Appointment (redundant as well).
* Louvre:
  * Everything is contained by the root container.
* Menso:
  * Invoices could be contained inside Customer.
* Musicmatic:
  * Tracks could be contained inside Album.
  * Odd "vATnumber" attribute name.
  * Album can be directly in MusicCatalog or can be contained through RegularUser.composedAlbums.
* OnlineTutoringSystem:
  * Enum literals all set to `0`.
* PizzaDeliveryWithEntertainment:
  * Employment could be contained in PizzaRestaurant.
* ProjectManagement:
  * ResearchGroupMember and WorkPackageLeader could go inside ResearchGroup.
* School
  * TeacherAssignment should be contained in Teacher or School?
* SellingGoods:
  * Odd vaTnumber name in Customer.
* Sightseeing:
  * Discount could be container in Visitor or GuidedTour.
* SmartHomeAutomationSystem:
  * Enum literals all set to `0`.
  * RuntimeElement uses a LocalTime instead of a full timestamp (type name was used over attribute name).
* Sober:
  * Involved could be contained in Car or in Accident.
* TutoringSystem:
  * CourseSubscription and TeachingAssistant should be contained in Course.
* TransportCompany:
  * Several typos got fixed here.
* TreatmentPlan:
  * Both Diagnosis and TreatmentPlan can contain Treatment. TreatmentPlan should not contain Treatment.
  * Consultation is not contained anywhere.
* University:
  * Participation should be contained in ResearchAssociate or Project.