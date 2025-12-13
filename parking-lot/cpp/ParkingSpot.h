// ParkingSpot.h
// Defines parking spot types with different vehicle compatibility rules
// Pattern: Inheritance hierarchy with abstract base class
// Purpose: Different spot types (Compact, Large, Bike, Handicapped, Electric) have different constraints

#pragma once
#include "Vehicle.h"
#include <string>
using namespace std;

/**
 * Abstract base class for all parking spot types
 * Each spot type defines which vehicles it can accommodate
 * Association: A ParkingSpot can hold one Vehicle at a time
 */
class ParkingSpot
{
protected:
    string spotId;                // Unique identifier (e.g., "F1-C01")
    bool isOccupied;              // Is a vehicle currently parked here?
    int floorNumber;              // Which floor this spot is on
    double distanceFromEntry;     // Distance from entry (used by parking strategies)
    bool isReserved;              // Is this spot reserved?
    Vehicle *vehicle;             // Currently parked vehicle (Association relationship)

public:
    ParkingSpot(string id, int floor, double distance)
        : spotId(id), floorNumber(floor), distanceFromEntry(distance),
          isReserved(false), isOccupied(false), vehicle(nullptr) {}

    virtual ~ParkingSpot() = default;

    // Pure virtual - each spot type defines compatibility rules
    virtual bool canFitVehicle(Vehicle *v) const = 0;
    virtual string getSpotCategory() const = 0;

    // Reservation management
    void reserve() { isReserved = true; }
    void unreserve() { isReserved = false; }
    bool getIsReserved() const { return isReserved; }

    // A spot is available if not occupied and not reserved
    bool isAvailable() const { return !isOccupied && !isReserved; }

    /**
     * Park a vehicle in this spot
     * Returns false if spot is occupied or vehicle doesn't fit
     */
    bool park(Vehicle *v)
    {
        if (isOccupied || !canFitVehicle(v))
        {
            return false;
        }
        vehicle = v;
        isOccupied = true;
        return true;
    }

    /**
     * Remove vehicle from this spot
     * Returns the vehicle that was parked
     */
    Vehicle *unpark()
    {
        Vehicle *temp = vehicle;
        vehicle = nullptr;
        isOccupied = false;
        return temp;
    }

    string getId() const { return spotId; }
    int getFloor() const { return floorNumber; }
    double getDistance() const { return distanceFromEntry; }
};

/**
 * CompactSpot - For small/medium non-electric vehicles
 * Accepts: Bike, Car (not ElectricCar, not Truck)
 */
class CompactSpot : public ParkingSpot
{
public:
    CompactSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}

    bool canFitVehicle(Vehicle *v) const override
    {
        bool isSmallorMedium = v->isMediumSized() || v->isSmallSized();
        bool isElectric = v->requiresCharging();

        // Accepts small/medium vehicles that don't require charging
        if (isSmallorMedium && !isElectric)
        {
            return true;
        }
        return false;
    }

    string getSpotCategory() const override { return "Compact"; }
};

/**
 * LargeSpot - For all non-electric vehicles regardless of size
 * Accepts: Bike, Car, Truck (not ElectricCar)
 */
class LargeSpot : public ParkingSpot
{
public:
    LargeSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}

    bool canFitVehicle(Vehicle *v) const override
    {
        bool isElectric = v->requiresCharging();

        // Accepts any non-electric vehicle (all sizes)
        if (!isElectric)
        {
            return true;
        }
        return false;
    }

    string getSpotCategory() const override { return "Large"; }
};

/**
 * BikeSpot - For small non-electric vehicles only
 * Accepts: Bike only
 */
class BikeSpot : public ParkingSpot
{
public:
    BikeSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}

    bool canFitVehicle(Vehicle *v) const override
    {
        bool isSmall = v->isSmallSized();
        bool isElectric = v->requiresCharging();

        // Only small, non-electric vehicles (bikes)
        if (isSmall && !isElectric)
        {
            return true;
        }
        return false;
    }

    string getSpotCategory() const override { return "Bike"; }
};
/**
 * HandicappedSpot - Accessible parking for medium non-electric vehicles
 * Accepts: Car only (reserved for handicapped users)
 */
class HandicappedSpot : public ParkingSpot
{
public:
    HandicappedSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}

    bool canFitVehicle(Vehicle *v) const override
    {
        bool isMedium = v->isMediumSized();
        bool isElectric = v->requiresCharging();

        // Only medium-sized, non-electric vehicles (regular cars)
        if (isMedium && !isElectric)
        {
            return true;
        }
        return false;
    }

    string getSpotCategory() const override { return "Handicapped"; }
};
/**
 * ElectricSpot - Charging station for electric vehicles
 * Accepts: ElectricCar only (any vehicle requiring charging)
 */
class ElectricSpot : public ParkingSpot
{
public:
    ElectricSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}

    bool canFitVehicle(Vehicle *v) const override
    {
        bool isElectric = v->requiresCharging();
        return isElectric; // Only electric vehicles
    }

    string getSpotCategory() const override { return "Electric"; }
};