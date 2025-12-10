#pragma once
#include "Vehicle.h"
#include <string>
using namespace std;

class ParkingSpot
{
protected:
    string spotId;
    bool isOccupied;
    int floorNumber;
    double distanceFromEntry;
    Vehicle *vehicle;

public:
    ParkingSpot(string id, int floor, double distance) : spotId(id), floorNumber(floor), distanceFromEntry(distance),
                                                         isOccupied(false), vehicle(nullptr) {}
    virtual ~ParkingSpot() = default;
    virtual bool canFitVehicle(Vehicle *v) const = 0;
    virtual string getSpotCategory() const = 0;
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
    Vehicle *unpark()
    {
        Vehicle *temp = vehicle;
        vehicle = nullptr;
        isOccupied = false;
        return temp;
    }
    bool isAvailable() const
    {
        return !isOccupied;
    }
    string getId() const { return spotId; }
    int getFloor() const { return floorNumber; }
    double getDistance() const { return distanceFromEntry; }
};

class CompactSpot : public ParkingSpot
{
public:
    CompactSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}
    bool canFitVehicle(Vehicle *v) const override
    {
        bool isSmallorMedium = v->isMediumSized() || v->isSmallSized();
        bool isElectric = v->requiresCharging();

        if (isSmallorMedium && !isElectric)
        {
            return true;
        }
        return false;
    }
    string getSpotCategory() const override
    {
        return "Compact";
    }
};

class LargeSpot : public ParkingSpot
{
public:
    LargeSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}
    bool canFitVehicle(Vehicle *v) const override
    {

        bool isElectric = v->requiresCharging();

        if (!isElectric)
        {
            return true;
        }
        return false;
    }
    string getSpotCategory() const override
    {
        return "Large";
    }
};

class BikeSpot : public ParkingSpot
{
public:
    BikeSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}
    bool canFitVehicle(Vehicle *v) const override
    {
        bool isSmall = v->isSmallSized();
        bool isElectric = v->requiresCharging();

        if (isSmall && !isElectric)
        {
            return true;
        }
        return false;
    }
    string getSpotCategory() const override
    {
        return "Bike";
    }
};
class HandicappedSpot : public ParkingSpot
{
public:
    HandicappedSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}
    bool canFitVehicle(Vehicle *v) const override
    {
        bool isMedium = v->isMediumSized();
        bool isElectric = v->requiresCharging();

        if (isMedium && !isElectric)
        {
            return true;
        }
        return false;
    }
    string getSpotCategory() const override
    {
        return "Handicapped";
    }
};
class ElectricSpot : public ParkingSpot
{
public:
    ElectricSpot(string id, int floor, double distance) : ParkingSpot(id, floor, distance) {}
    bool canFitVehicle(Vehicle *v) const override
    {

        bool isElectric = v->requiresCharging();
        return isElectric;
    }
    string getSpotCategory() const override
    {
        return "Electric";
    }
};