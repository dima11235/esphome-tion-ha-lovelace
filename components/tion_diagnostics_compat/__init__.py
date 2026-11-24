"""Restore formatting helpers still used by dentra's Tion driver on ESPHome 2026.11."""
import esphome.codegen as cg
import esphome.config_validation as cv

CONFIG_SCHEMA = cv.Schema({})


async def to_code(config):
    # Driver .cpp files need the declarations too, not just generated main.cpp.
    cg.add_build_flag("-include esphome/components/tion_diagnostics_compat/compat.h")
