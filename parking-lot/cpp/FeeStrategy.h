#pragma once
#include "ParkingTicket.h"
#include <map>
using namespace std;

class FeeStrategy
{
public:
    virtual ~FeeStrategy() = default;
    virtual double calculateFee(ParkingTicket *ticket) = 0;
    virtual string getName() const = 0;
};

class HourlyFeeStrategy : public FeeStrategy
{
private:
    double ratePerHour;

public:
    HourlyFeeStrategy(double rate = 50.0) : ratePerHour(rate) {}
    double calculateFee(ParkingTicket *ticket) override
    {
        double hours = ticket->getDurationInHours();
        if (hours < 1)
            hours = 1;
        return hours * ratePerHour;
    }
    string getName() const override
    {
        return "Hourly Flat Rate";
    }
};

class VehicleBasedFeeStrategy : public FeeStrategy
{
private:
    struct PricingTier
    {
        double baseCharge; // First hour
        double hourlyRate; // Additional hours
    };

    map<string, PricingTier> pricing; // Map vehicle size to pricing
    double chargingFee;

public:
    VehicleBasedFeeStrategy() : chargingFee(50.0)
    {
        pricing["small"] = {30.0, 50.0};
        pricing["medium"] = {50.0, 80.0};
        pricing["large"] = {100.0, 100.0};
    }

    double calculateFee(ParkingTicket *ticket) override
    {
        Vehicle *vehicle = ticket->getVehicle();
        double hours = ticket->getDurationInHours();

        if (hours < 1)
            hours = 1; // Minimum 1 hour

        // TODO: Determine vehicle size (small/medium/large)
        string size;
        if (vehicle->isSmallSized())
            size = "small";
        else if (vehicle->isMediumSized())
            size = "medium";
        else if (vehicle->isLargeSized())
            size = "large";
        else
            size = "medium"; // Default

        // TODO: Get pricing tier for this size
        PricingTier tier = pricing[size];

        // TODO: Calculate fee = baseCharge + (hours-1) * hourlyRate
        double fee = tier.baseCharge;
        if (hours > 1)
        {
            fee += (hours - 1) * tier.hourlyRate;
        }

        if (vehicle->requiresCharging())
        {
            fee += chargingFee;
        }

        return fee;
    }

    string getName() const override
    {
        return "Vehicle-Based Pricing";
    }
};