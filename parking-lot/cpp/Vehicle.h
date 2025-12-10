#pragma once

#include <string>
using namespace std;

class Vehicle
{
protected:
    string licenseNumber;

public:
    Vehicle(string license) : licenseNumber(license) {}
    virtual ~Vehicle() = default;

    virtual bool isSmallSized() const = 0;
    virtual bool isMediumSized() const = 0;
    virtual bool isLargeSized() const = 0;
    virtual bool requiresCharging() const = 0;
    virtual string getVehicleCategory() const = 0;

    string getLicenseNumber() const { return licenseNumber; }
};

class Car : public Vehicle
{
public:
    Car(string license) : Vehicle(license) {}
    bool isSmallSized() const override
    {
        return false;
    }
    bool isMediumSized() const override
    {
        return true;
    }
    bool isLargeSized() const override
    {
        return false;
    }
    bool requiresCharging() const override
    {
        return false;
    }
    string getVehicleCategory() const override
    {
        return "Car";
    }
};

class Truck : public Vehicle
{
public:
    Truck(string license) : Vehicle(license) {}
    bool isSmallSized() const override
    {
        return false;
    }
    bool isMediumSized() const override
    {
        return false;
    }
    bool isLargeSized() const override
    {
        return true;
    }
    bool requiresCharging() const override
    {
        return false;
    }
    string getVehicleCategory() const override
    {
        return "Truck";
    }
};

class Bike : public Vehicle
{
public:
    Bike(string license) : Vehicle(license) {}
    bool isSmallSized() const override
    {
        return true;
    }
    bool isMediumSized() const override
    {
        return false;
    }
    bool isLargeSized() const override
    {
        return false;
    }
    bool requiresCharging() const override
    {
        return false;
    }
    string getVehicleCategory() const override
    {
        return "Bike";
    }
};

class ElectricCar : public Vehicle
{
public:
    ElectricCar(string license) : Vehicle(license) {}
    bool isSmallSized() const override
    {
        return false;
    }
    bool isMediumSized() const override
    {
        return true;
    }
    bool isLargeSized() const override
    {
        return false;
    }
    bool requiresCharging() const override
    {
        return true;
    }
    string getVehicleCategory() const override
    {
        return "ElectricCar";
    }
};
