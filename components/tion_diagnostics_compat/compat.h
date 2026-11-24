#pragma once

// ESPHome 2026.11 removed these heap-formatting helpers. The external Tion
// driver still uses them. Opt-in with the diagnostic package only; no I/O.
#ifdef __cplusplus
#include "esphome/core/helpers.h"
#include <cstdarg>
#include <cstdio>
#include <string>
#include <vector>

namespace esphome {
inline std::string format_hex_pretty(const uint8_t *data, size_t size,
                                    char separator = '.', bool show_length = true) {
  static constexpr char HEX[] = "0123456789ABCDEF";
  std::string result;
  result.reserve(size * 3 + 16);
  for (size_t i = 0; i < size; ++i) {
    if (i && separator) result.push_back(separator);
    result.push_back(HEX[data[i] >> 4]);
    result.push_back(HEX[data[i] & 15]);
  }
  if (show_length && size > 4) {
    char suffix[24];
    std::snprintf(suffix, sizeof(suffix), " (%u)", static_cast<unsigned>(size));
    result.append(suffix);
  }
  return result;
}

inline std::string format_hex_pretty(const std::vector<uint8_t> &data,
                                    char separator = '.', bool show_length = true) {
  return format_hex_pretty(data.data(), data.size(), separator, show_length);
}

inline std::string str_sprintf(const char *format, ...) __attribute__((format(printf, 1, 2)));
inline std::string str_sprintf(const char *format, ...) {
  va_list args;
  va_start(args, format);
  va_list copy;
  va_copy(copy, args);
  int length = std::vsnprintf(nullptr, 0, format, copy);
  va_end(copy);
  std::string result;
  if (length > 0) {
    result.resize(length + 1);
    std::vsnprintf(result.data(), result.size(), format, args);
    result.resize(length);
  }
  va_end(args);
  return result;
}
}  // namespace esphome
#endif
