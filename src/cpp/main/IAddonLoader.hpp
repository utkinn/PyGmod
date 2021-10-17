#pragma once

namespace pygmod::init
{
    class IAddonLoader
    {
    public:
        virtual void load() = 0;
    };
}