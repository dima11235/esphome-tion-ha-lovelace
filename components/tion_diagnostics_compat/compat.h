#pragma once

// Since ESPHome 2026.11 heap-formatting helpers live in alloc_helpers.h.
// Tion still includes helpers.h. Make the declarations visible in its .cpp
// files too. No replacement implementations or changes to the driver.
#ifdef __cplusplus
#include "esphome/core/alloc_helpers.h"
#endif
