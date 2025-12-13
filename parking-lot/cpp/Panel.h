// Panel.h
#pragma once
#include "Floor.h"
using namespace std;

class EntryPanel
{
private:
    static int panelCounter;
    int panelId;
    Floor *floor;

public:
    EntryPanel(Floor *f) : floor(f), panelId(++panelCounter) {}

    int getId() const { return panelId; }
    Floor *getFloor() const { return floor; }
};

int EntryPanel::panelCounter = 0;

class ExitPanel
{
private:
    static int panelCounter;
    int panelId;
    Floor *floor;

public:
    ExitPanel(Floor *f) : floor(f), panelId(++panelCounter) {}

    int getId() const { return panelId; }
    Floor *getFloor() const { return floor; }
};

int ExitPanel::panelCounter = 0;