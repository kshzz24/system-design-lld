// Vehicle.h
// Defines the Vehicle class hierarchy using polymorphism
// Pattern: Inheritance hierarchy with abstract base class
// Purpose: Supports different vehicle types with varying size and charging requirements

#pragma once

#include <string>
using namespace std;

/**
 * Abstract base class representing any vehicle that can be parked
 * Uses polymorphism to define different vehicle characteristics
 */
class Vehicle
{
protected:
    string licenseNumber; // Unique identifier for each vehicle

public:
    Vehicle(string license) : licenseNumber(license) {}
    virtual ~Vehicle() = default;

    // Pure virtual methods - each derived class must implement these
    virtual bool isSmallSized() const = 0;      // For bikes
    virtual bool isMediumSized() const = 0;     // For cars
    virtual bool isLargeSized() const = 0;      // For trucks
    virtual bool requiresCharging() const = 0;   // For electric vehicles
    virtual string getVehicleCategory() const = 0; // Returns vehicle type name

    string getLicenseNumber() const { return licenseNumber; }
};

/**
 * Car - Medium-sized, non-electric vehicle
 * Can fit in: CompactSpot, LargeSpot, HandicappedSpot
 */
class Car : public Vehicle
{
public:
    Car(string license) : Vehicle(license) {}
    bool isSmallSized() const override { return false; }
    bool isMediumSized() const override { return true; }    // Cars are medium-sized
    bool isLargeSized() const override { return false; }
    bool requiresCharging() const override { return false; } // Regular car, no charging
    string getVehicleCategory() const override { return "Car"; }
};

/**
 * Truck - Large-sized, non-electric vehicle
 * Can fit in: LargeSpot only
 */
class Truck : public Vehicle
{
public:
    Truck(string license) : Vehicle(license) {}
    bool isSmallSized() const override { return false; }
    bool isMediumSized() const override { return false; }
    bool isLargeSized() const override { return true; }     // Trucks are large-sized
    bool requiresCharging() const override { return false; }
    string getVehicleCategory() const override { return "Truck"; }
};

/**
 * Bike - Small-sized, non-electric vehicle
 * Can fit in: BikeSpot, CompactSpot, LargeSpot
 */
class Bike : public Vehicle
{
public:
    Bike(string license) : Vehicle(license) {}
    bool isSmallSized() const override { return true; }     // Bikes are small-sized
    bool isMediumSized() const override { return false; }
    bool isLargeSized() const override { return false; }
    bool requiresCharging() const override { return false; }
    string getVehicleCategory() const override { return "Bike"; }
};

/**
 * ElectricCar - Medium-sized, electric vehicle requiring charging
 * Can fit in: ElectricSpot only (needs charging facility)
 */
class ElectricCar : public Vehicle
{
public:
    ElectricCar(string license) : Vehicle(license) {}
    bool isSmallSized() const override { return false; }
    bool isMediumSized() const override { return true; }
    bool isLargeSized() const override { return false; }
    bool requiresCharging() const override { return true; }  // Requires electric charging
    string getVehicleCategory() const override { return "ElectricCar"; }
};
