-- Patching isfunction() to treat Python functions and tables with __call metamethod as actual functions
local oldIsfunction = isfunction
function isfunction(o)
    return oldIsfunction(o) or type(o) == "PyCallable" or (istable(o) and getmetatable(o) ~= nil and getmetatable(o).__call ~= nil)
end

-- Continuing to the original init
include("original_init.lua")