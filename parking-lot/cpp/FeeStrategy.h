// FeeStrategy.h
// Implements Strategy Pattern for different fee calculation methods
// Pattern: Strategy Pattern
// Purpose: Allows runtime selection of fee algorithms (Hourly flat vs Vehicle-based pricing)

#pragma once
#include "ParkingTicket.h"
#include <map>
using namespace std;

/**
 * Abstract Strategy class for parking fee calculation
 * Defines the interface for different pricing models
 * Pattern: Strategy Pattern - allows switching pricing models at runtime
 */
class FeeStrategy
{
public:
    virtual ~FeeStrategy() = default;

    // Calculate parking fee based on ticket information
    virtual double calculateFee(ParkingTicket *ticket) = 0;

    virtual string getName() const = 0;
};

/**
 * HourlyFeeStrategy - Simple flat rate per hour for all vehicles
 * Use case: Simple pricing, same rate regardless of vehicle type
 */
class HourlyFeeStrategy : public FeeStrategy
{
private:
    double ratePerHour; // Fixed rate per hour

public:
    HourlyFeeStrategy(double rate = 50.0) : ratePerHour(rate) {}

    double calculateFee(ParkingTicket *ticket) override
    {
        double hours = ticket->getDurationInHours();
        if (hours < 1)
            hours = 1; // Minimum 1 hour charge

        return hours * ratePerHour; // Simple multiplication
    }

    string getName() const override { return "Hourly Flat Rate"; }
};

/**
 * VehicleBasedFeeStrategy - Different pricing based on vehicle size and features
 * Use case: Differentiated pricing, larger vehicles pay more, electric vehicles pay charging fee
 * Pricing model: Base charge for first hour + hourly rate for additional hours
 */
class VehicleBasedFeeStrategy : public FeeStrategy
{
private:
    struct PricingTier
    {
        double baseCharge; // First hour charge
        double hourlyRate; // Additional hours rate
    };

    map<string, PricingTier> pricing; // Map vehicle size to pricing tier
    double chargingFee;               // Extra fee for electric vehicle charging

public:
    VehicleBasedFeeStrategy() : chargingFee(50.0)
    {
        // Small vehicles (bikes): Lower pricing
        pricing["small"] = {30.0, 50.0};
        // Medium vehicles (cars): Moderate pricing
        pricing["medium"] = {50.0, 80.0};
        // Large vehicles (trucks): Higher pricing
        pricing["large"] = {100.0, 100.0};
    }

    double calculateFee(ParkingTicket *ticket) override
    {
        Vehicle *vehicle = ticket->getVehicle();
        double hours = ticket->getDurationInHours();

        if (hours < 1)
            hours = 1; // Minimum 1 hour charge

        // Determine vehicle size category
        string size;
        if (vehicle->isSmallSized())
            size = "small";
        else if (vehicle->isMediumSized())
            size = "medium";
        else if (vehicle->isLargeSized())
            size = "large";
        else
            size = "medium"; // Default to medium

        // Get pricing tier for this vehicle size
        PricingTier tier = pricing[size];

        // Calculate: baseCharge + (additional hours * hourlyRate)
        double fee = tier.baseCharge;
        if (hours > 1)
        {
            fee += (hours - 1) * tier.hourlyRate;
        }

        // Add charging fee for electric vehicles
        if (vehicle->requiresCharging())
        {
            fee += chargingFee;
        }

        return fee;
    }

    string getName() const override { return "Vehicle-Based Pricing"; }
};