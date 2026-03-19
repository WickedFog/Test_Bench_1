local function init() end

local function run()
  for i=0, LED_STRIP_LENGTH - 1, 1 do
    setRGBLedColor(i, 255, 0, 0)
  end
  applyRGBLedColors()
end

local function background() end

return { run=run, background=background, init=init }