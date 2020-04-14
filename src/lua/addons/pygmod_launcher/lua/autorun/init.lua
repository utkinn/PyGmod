-- First stage of PyGmod init. This script loads pygmod.dll.

local success, errorMessage = pcall(require, 'pygmod')  -- See src/cpp/client and src/cpp/server
if not success then
    error('[PyGmod|init.lua|ERROR] Problems with loading PyGmod C++ module. Make sure PyGmod is installed correctly. ('..errorMessage..')')
end
