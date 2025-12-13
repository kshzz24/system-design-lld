// main.cpp
// Demonstrates the Parking Lot System with comprehensive test scenarios
// Tests: Regular parking, strategy switching, reservations, payments, fee strategies

#include "ParkingLot.h"
#include <unistd.h>
using namespace std;

int main() {
    cout << "========== PARKING LOT SYSTEM ==========\n\n";

    // Get singleton instance (only one parking lot can exist)
    ParkingLot* parkingLot = ParkingLot::getInstance();
    
    // ========== SETUP PARKING LOT ==========
    // Create Floor 1 with diverse spot types
    Floor* floor1 = new Floor(1);
    floor1->addSpot(new BikeSpot("F1-B01", 1, 10.0));       // Distance: 10m from entry
    floor1->addSpot(new CompactSpot("F1-C01", 1, 20.0));    // Distance: 20m
    floor1->addSpot(new LargeSpot("F1-L01", 1, 30.0));      // Distance: 30m
    floor1->addSpot(new ElectricSpot("F1-E01", 1, 25.0));   // Distance: 25m

    // Create Floor 2 with additional spots
    Floor* floor2 = new Floor(2);
    floor2->addSpot(new CompactSpot("F2-C01", 2, 35.0));
    floor2->addSpot(new LargeSpot("F2-L01", 2, 40.0));

    // Add floors to parking lot
    parkingLot->addFloor(floor1);
    parkingLot->addFloor(floor2);

    // Add entry/exit panels
    parkingLot->addEntryPanel(new EntryPanel(floor1));
    parkingLot->addExitPanel(new ExitPanel(floor1));

    cout << "✓ Parking lot setup complete\n";
    parkingLot->displayStatus();
    
    // ========== TEST 1: REGULAR PARKING ==========
    // Test parking with default NearestFirstStrategy
    cout << "\n\n========== TEST 1: REGULAR PARKING ==========\n";
    Vehicle* car = new Car("KA01-1234");
    Vehicle* bike = new Bike("KA02-5678");

    // Park vehicles using default strategy (Nearest First)
    ParkingTicket* t1 = parkingLot->parkVehicle(car);
    ParkingTicket* t2 = parkingLot->parkVehicle(bike);

    parkingLot->displayStatus();
    
    // ========== TEST 2: CHANGE PARKING STRATEGY ==========
    // Demonstrate Strategy Pattern - switch algorithm at runtime
    cout << "\n\n========== TEST 2: CHANGE STRATEGY ==========\n";
    parkingLot->setParkingStrategy(new BestFitStrategy());  // Switch to BestFit

    Vehicle* truck = new Truck("KA03-9012");
    ParkingTicket* t3 = parkingLot->parkVehicle(truck);  // Uses BestFit strategy
    
    // ========== TEST 3: RESERVATION SYSTEM ==========
    // Test advance reservation and parking with reservation
    cout << "\n\n========== TEST 3: RESERVATION ==========\n";
    Vehicle* car2 = new Car("KA04-3456");
    Reservation* reservation = parkingLot->reserveSpot(car2, 2);  // Reserve for 2 hours

    parkingLot->displayStatus();

    cout << "\nParking with reservation...\n";
    ParkingTicket* t4 = parkingLot->parkVehicle(car2, reservation->getId());
    
    // ========== TEST 4: UNPARKING & PAYMENT ==========
    // Test payment processing with HourlyFeeStrategy
    cout << "\n\n========== TEST 4: UNPARKING ==========\n";
    sleep(2);  // Simulate 2 seconds of parking (will be calculated as hours)

    if (t1) {
        // Unpark car - calculates fee using HourlyFeeStrategy
        Payment* p1 = parkingLot->unparkVehicle(t1->getId(), "Credit Card");
        delete p1;
    }

    if (t2) {
        // Unpark bike - same pricing as car (hourly flat rate)
        Payment* p2 = parkingLot->unparkVehicle(t2->getId(), "Cash");
        delete p2;
    }
    
    // ========== TEST 5: CHANGE FEE STRATEGY ==========
    // Demonstrate Strategy Pattern - switch fee calculation algorithm
    cout << "\n\n========== TEST 5: VEHICLE-BASED PRICING ==========\n";
    parkingLot->setFeeStrategy(new VehicleBasedFeeStrategy());  // Switch to vehicle-based pricing

    if (t3) {
        // Unpark truck - will pay more due to vehicle-based pricing (large vehicle)
        Payment* p3 = parkingLot->unparkVehicle(t3->getId(), "Debit Card");
        delete p3;
    }

    // ========== FINAL STATUS & CLEANUP ==========
    parkingLot->displayStatus();

    cout << "\n✓ Total Revenue: $" << parkingLot->getTotalRevenue() << "\n";

    // Cleanup dynamically allocated vehicles
    delete car; delete bike; delete truck; delete car2;

    cout << "\n========== SYSTEM TEST COMPLETE ==========\n";
    return 0;
}