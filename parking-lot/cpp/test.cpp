// // test.cpp
// #include "Vehicle.h"
// #include "ParkingSpot.h"
// #include <iostream>
// using namespace std;

// int main()
// {
//     cout << "========== TESTING INTERFACE-BASED DESIGN ==========\n\n";

//     // Create vehicles
//     Vehicle *car = new Car("KA01-1234");
//     Vehicle *bike = new Bike("KA02-5678");
//     Vehicle *truck = new Truck("KA03-9012");
//     Vehicle *eCar = new ElectricCar("KA04-3456");

//     // Test 1: Vehicle interface
//     cout << "Test 1: Vehicle Properties\n";
//     cout << "Car category: " << car->getVehicleCategory() << "\n";
//     cout << "Car is medium? " << car->isMediumSized() << "\n";
//     cout << "Bike is small? " << bike->isSmallSized() << "\n";
//     cout << "ECar needs charging? " << eCar->requiresCharging() << "\n";
//     cout << "Truck is large? " << truck->isLargeSized() << "\n";

//     // Create spots
//     ParkingSpot *compactSpot = new CompactSpot("C01", 1, 10.0);
//     ParkingSpot *bikeSpot = new BikeSpot("B01", 1, 5.0);
//     ParkingSpot *largeSpot = new LargeSpot("L01", 1, 20.0);
//     ParkingSpot *electricSpot = new ElectricSpot("E01", 1, 15.0);

//     // Test 2: Spot compatibility (Polymorphism in action!)
//     cout << "\nTest 2: Spot Compatibility (No Enums!)\n";
//     cout << "CompactSpot can fit car? " << compactSpot->canFitVehicle(car) << " (should be 1)\n";
//     cout << "CompactSpot can fit bike? " << compactSpot->canFitVehicle(bike) << " (should be 1)\n";
//     cout << "CompactSpot can fit truck? " << compactSpot->canFitVehicle(truck) << " (should be 0)\n";
//     cout << "CompactSpot can fit eCar? " << compactSpot->canFitVehicle(eCar) << " (should be 0)\n";

//     cout << "\nBikeSpot can fit bike? " << bikeSpot->canFitVehicle(bike) << " (should be 1)\n";
//     cout << "BikeSpot can fit car? " << bikeSpot->canFitVehicle(car) << " (should be 0)\n";

//     cout << "\nLargeSpot can fit truck? " << largeSpot->canFitVehicle(truck) << " (should be 1)\n";
//     cout << "LargeSpot can fit eCar? " << largeSpot->canFitVehicle(eCar) << " (should be 0)\n";

//     cout << "\nElectricSpot can fit eCar? " << electricSpot->canFitVehicle(eCar) << " (should be 1)\n";
//     cout << "ElectricSpot can fit car? " << electricSpot->canFitVehicle(car) << " (should be 0)\n";

//     // Test 3: Park and unpark
//     cout << "\nTest 3: Park Operations\n";
//     cout << "Parking car in compact spot: " << compactSpot->park(car) << "\n";
//     cout << "Compact spot available? " << compactSpot->isAvailable() << " (should be 0)\n";
//     cout << "Trying to park bike in same spot: " << compactSpot->park(bike) << " (should be 0)\n";

//     Vehicle *unparked = compactSpot->unpark();
//     cout << "Unparked vehicle: " << unparked->getLicenseNumber() << "\n";
//     cout << "Compact spot available now? " << compactSpot->isAvailable() << " (should be 1)\n";

//     // Cleanup
//     delete car;
//     delete bike;
//     delete truck;
//     delete eCar;
//     delete compactSpot;
//     delete bikeSpot;
//     delete largeSpot;
//     delete electricSpot;

//     cout << "\n✓ All tests passed!\n";
//     return 0;
// }





/// --------------------------------------------------------------------------------------




/// testing ticket
// test_ticket.cpp
// #include "ParkingTicket.h"
// #include <iostream>
// #include <unistd.h> // for sleep()
// using namespace std;

// int main()
// {
//     cout << "========== TESTING PARKING TICKET ==========\n\n";

//     // Create vehicles and spot
//     Vehicle *car = new Car("KA01-1234");
//     ParkingSpot *spot = new CompactSpot("C01", 1, 10.0);

//     // Park vehicle
//     spot->park(car);

//     // Test 1: Create ticket
//     ParkingTicket *ticket1 = new ParkingTicket(car, spot);
//     cout << "Test 1: Ticket Created\n";
//     ticket1->printTicket();
//     cout << "Is active? " << ticket1->getIsActive() << " (should be 1)\n";

//     // Test 2: Multiple tickets have unique IDs
//     Vehicle *bike = new Bike("KA02-5678");
//     ParkingSpot *bikeSpot = new BikeSpot("B01", 1, 5.0);
//     bikeSpot->park(bike);
//     ParkingTicket *ticket2 = new ParkingTicket(bike, bikeSpot);

//     cout << "\nTest 2: Unique Ticket IDs\n";
//     cout << "Ticket 1 ID: " << ticket1->getId() << "\n";
//     cout << "Ticket 2 ID: " << ticket2->getId() << "\n";
//     cout << "IDs are different? " << (ticket1->getId() != ticket2->getId()) << " (should be 1)\n";

//     // Test 3: Duration calculation
//     cout << "\nTest 3: Duration Calculation\n";
//     cout << "Waiting 3 seconds...\n";
//     sleep(3); // Simulate 3 seconds parking

//     cout << "Duration before exit: " << ticket1->getDurationInHours() << " hours\n";

//     ticket1->markExit();
//     cout << "Duration after exit: " << ticket1->getDurationInHours() << " hours\n";
//     cout << "Is active after exit? " << ticket1->getIsActive() << " (should be 0)\n";

//     // Test 4: Verify ticket data
//     cout << "\nTest 4: Ticket Data\n";
//     cout << "Vehicle license: " << ticket1->getVehicle()->getLicenseNumber() << "\n";
//     cout << "Spot ID: " << ticket1->getSpot()->getId() << "\n";
//     cout << "Floor: " << ticket1->getSpot()->getFloor() << "\n";

//     // Cleanup
//     delete ticket1;
//     delete ticket2;
//     delete car;
//     delete bike;
//     delete spot;
//     delete bikeSpot;

//     cout << "\n✓ All ticket tests passed!\n";
//     return 0;
// }
