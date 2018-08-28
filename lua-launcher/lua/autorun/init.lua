local success = pcall(require, 'gpython')
if not success then
    error('[GPython] ERROR: GPython binary module is not installed or installed incorrectly.')
end
