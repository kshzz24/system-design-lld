// main.cpp
#include "ParkingLot.h"
#include <unistd.h>
using namespace std;

int main() {
    cout << "========== PARKING LOT SYSTEM ==========\n\n";
    
    // Get singleton instance
    ParkingLot* parkingLot = ParkingLot::getInstance();
    
    // Setup Floor 1
    Floor* floor1 = new Floor(1);
    floor1->addSpot(new BikeSpot("F1-B01", 1, 10.0));
    floor1->addSpot(new CompactSpot("F1-C01", 1, 20.0));
    floor1->addSpot(new LargeSpot("F1-L01", 1, 30.0));
    floor1->addSpot(new ElectricSpot("F1-E01", 1, 25.0));
    
    // Setup Floor 2
    Floor* floor2 = new Floor(2);
    floor2->addSpot(new CompactSpot("F2-C01", 2, 35.0));
    floor2->addSpot(new LargeSpot("F2-L01", 2, 40.0));
    
    parkingLot->addFloor(floor1);
    parkingLot->addFloor(floor2);
    
    // Add panels
    parkingLot->addEntryPanel(new EntryPanel(floor1));
    parkingLot->addExitPanel(new ExitPanel(floor1));
    
    cout << "✓ Parking lot setup complete\n";
    parkingLot->displayStatus();
    
    // Test 1: Regular parking
    cout << "\n\n========== TEST 1: REGULAR PARKING ==========\n";
    Vehicle* car = new Car("KA01-1234");
    Vehicle* bike = new Bike("KA02-5678");
    
    ParkingTicket* t1 = parkingLot->parkVehicle(car);
    ParkingTicket* t2 = parkingLot->parkVehicle(bike);
    
    parkingLot->displayStatus();
    
    // Test 2: Change strategy
    cout << "\n\n========== TEST 2: CHANGE STRATEGY ==========\n";
    parkingLot->setParkingStrategy(new BestFitStrategy());
    
    Vehicle* truck = new Truck("KA03-9012");
    ParkingTicket* t3 = parkingLot->parkVehicle(truck);
    
    // Test 3: Reservation
    cout << "\n\n========== TEST 3: RESERVATION ==========\n";
    Vehicle* car2 = new Car("KA04-3456");
    Reservation* reservation = parkingLot->reserveSpot(car2, 2);
    
    parkingLot->displayStatus();
    
    cout << "\nParking with reservation...\n";
    ParkingTicket* t4 = parkingLot->parkVehicle(car2, reservation->getId());
    
    // Test 4: Simulate time and unpark
    cout << "\n\n========== TEST 4: UNPARKING ==========\n";
    sleep(2);
    
    if (t1) {
        Payment* p1 = parkingLot->unparkVehicle(t1->getId(), "Credit Card");
        delete p1;
    }
    
    if (t2) {
        Payment* p2 = parkingLot->unparkVehicle(t2->getId(), "Cash");
        delete p2;
    }
    
    // Test 5: Change fee strategy
    cout << "\n\n========== TEST 5: VEHICLE-BASED PRICING ==========\n";
    parkingLot->setFeeStrategy(new VehicleBasedFeeStrategy());
    
    if (t3) {
        Payment* p3 = parkingLot->unparkVehicle(t3->getId(), "Debit Card");
        delete p3;
    }
    
    // Final status
    parkingLot->displayStatus();
    
    cout << "\n✓ Total Revenue: $" << parkingLot->getTotalRevenue() << "\n";
    
    // Cleanup
    delete car; delete bike; delete truck; delete car2;
    
    cout << "\n========== SYSTEM TEST COMPLETE ==========\n";
    return 0;
}