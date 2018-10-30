local success, errorMessage = pcall(require, 'pygmod')
if not success then
    error('[PyGmod] ERROR: PyGmod binary module is not installed or installed incorrectly. ('..errorMessage..')')
end
