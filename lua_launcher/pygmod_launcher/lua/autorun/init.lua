-- First stage of PyGmod init. This script loads pygmod.dll.

local success, errorMessage = pcall(require, 'pygmod')  -- See bin_modules\client\main.cpp, bin_modules\server\main.cpp
if not success then
    error('[PyGmod] ERROR: PyGmod binary module is not installed or installed incorrectly. ('..errorMessage..')')
end
