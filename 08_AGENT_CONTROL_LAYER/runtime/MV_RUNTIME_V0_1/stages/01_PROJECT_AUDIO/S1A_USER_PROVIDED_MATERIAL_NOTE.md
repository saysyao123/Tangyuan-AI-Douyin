# S1A Note — User-Provided Material Exception

Date: 2026-09-24

## Purpose

Record a one-run exception without changing the normal S1A architecture.

## Current run

Selected Song Family:
`若爱有尽头`

Normal autonomous acquisition status before this run:
`SOURCE_COVERAGE_BLOCKED`

User then provided:
`“如果爱有尽头 怎么想念没有”.mp4`

This file is treated as:
`USER_PROVIDED_MEDIA_FALLBACK`

## Important boundary

This fallback allows the current S1 test to continue into S1B/S1C/S1D.

It does NOT mean:
- S1A autonomous acquisition is solved for this Song Family;
- user upload becomes the default production path;
- the previous S1A source-coverage research should be deleted.

## S1A standing rule

Normal path remains:
autonomous acquisition -> version/source validation -> analyzable media.

User-provided media remains:
exception fallback only.

## Current effect

S1A research:
kept separate / still requires future source-adapter work.

Current S1 run:
allowed to continue using the provided media as the authoritative test source.
